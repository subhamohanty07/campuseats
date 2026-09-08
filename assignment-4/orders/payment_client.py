import logging
import os
import random
import time

import requests

logger = logging.getLogger(__name__)

# Payments Service address must come from an environment variable.
PAYMENTS_URL = os.getenv("PAYMENTS_URL")

CONNECT_TIMEOUT = 2
READ_TIMEOUT = 3

MAX_RETRIES = 3
BASE_BACKOFF = 0.2


def charge_payment(order_id, amount, idempotency_key):
    """
    Calls the Payments Service with timeout and retry handling.

    Retry conditions:
    - Network errors
    - Connection/read timeouts
    - HTTP 5xx responses

    No retry:
    - HTTP 4xx responses

    The same Idempotency-Key is sent on every retry so that a
    retried payment request cannot accidentally create duplicates.
    """

    if not PAYMENTS_URL:
        logger.error("PAYMENTS_URL environment variable is not configured.")
        return {
            "success": False,
            "fallback": True,
            "reason": "Payments Service address is not configured"
        }

    payload = {
        "orderId": order_id,
        "amount": amount,
        "currency": "INR",
        "paymentMethod": "CARD",
    }

    headers = {
        "Idempotency-Key": idempotency_key
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(
                "Calling Payments Service: order=%s attempt=%s",
                order_id,
                attempt
            )

            response = requests.post(
                PAYMENTS_URL,
                json=payload,
                headers=headers,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
            )

            if 400 <= response.status_code < 500:
                logger.warning(
                    "Payments Service returned %s; not retrying.",
                    response.status_code
                )
                return {
                    "success": False,
                    "fallback": False,
                    "reason": f"Payments Service returned {response.status_code}"
                }

            if response.status_code >= 500:
                logger.warning(
                    "Payments Service returned %s on attempt %s.",
                    response.status_code,
                    attempt
                )

                if attempt < MAX_RETRIES:
                    sleep_with_backoff(attempt)
                    continue

                return {
                    "success": False,
                    "fallback": True,
                    "reason": "Payments Service unavailable after retries"
                }

            if 200 <= response.status_code < 300:
                data = response.json()

                return {
                    "success": True,
                    "fallback": False,
                    "transactionId": data.get("transactionId"),
                    "message": data.get(
                        "message",
                        "Payment successful"
                    )
                }

            return {
                "success": False,
                "fallback": True,
                "reason": f"Unexpected payment status {response.status_code}"
            }

        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError
        ) as exc:

            logger.warning(
                "Payments Service network/timeout failure "
                "on attempt %s: %s",
                attempt,
                exc
            )

            if attempt < MAX_RETRIES:
                sleep_with_backoff(attempt)
                continue

            return {
                "success": False,
                "fallback": True,
                "reason": "Payments Service unavailable after retries"
            }

        except requests.exceptions.RequestException as exc:

            logger.error(
                "Unexpected Payments Service error: %s",
                exc
            )

            return {
                "success": False,
                "fallback": True,
                "reason": "Unexpected Payments Service error"
            }


def sleep_with_backoff(attempt):
    """
    Exponential backoff with jitter.

    Example:
    attempt 1 → roughly 0.2 seconds
    attempt 2 → roughly 0.4 seconds
    attempt 3 → roughly 0.8 seconds
    """

    exponential_delay = BASE_BACKOFF * (2 ** (attempt - 1))

    jitter = random.uniform(
        0,
        exponential_delay * 0.25
    )

    delay = exponential_delay + jitter

    logger.info(
        "Retrying Payments Service after %.3f seconds.",
        delay
    )

    time.sleep(delay)