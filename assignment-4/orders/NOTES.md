# CS543 Web Services — Assignment 4
## Rebuilding CampusEats Orders Service in REST

**Team Members**

| No. | Name | Roll Number |
|---:|---|---|
| 1 | Mahi Verma | 20252651032 |
| 2 | Subham Kumar Mohanty | 20252651057 |
| 3 | Abhishek Jadhao | 20252651003 |
| 4 | Harsh N Shende | 20252651023 |
| 5 | Rishabh Mishra | 20252651041 |

**Selected Service:** Orders Service  
**Technology:** Python + Flask + OpenAPI 3.0.3  
**Repository folder:** `assignment-4/orders/`

---

# 1. Part A — REST Service Design

## A1. Selected Service and Boundary

The selected CampusEats service is the **Orders Service**. According to the service boundary defined earlier, Orders owns carts, orders, and order status. The Orders Service does not directly access the databases of Catalogue or Payments; it communicates with those services through their published contracts.

For this assignment, the implementation focuses on orders while preserving the existing ownership boundary.

## A2. Operations We Would Have Written as SOAP

Before designing the REST resources, the equivalent SOAP/WSDL-style operations can be described as:

1. `createOrder(studentId, addressId, items)`
2. `getOrder(orderId)`
3. `listOrdersByStatus(status)`
4. `cancelOrder(orderId)`

These operation names are only the starting point. The REST design replaces operation-oriented URLs with resource-oriented URLs.

## A3. Durable Nouns

The durable nouns identified from the operations are:

- **orders** — the main resource owned by the Orders Service.
- **cancellation** — a state-changing sub-resource associated with an order.

The verbs `create`, `get`, `list`, and `cancel` do not appear in the URLs. The collection resource is `/orders`, an individual order is `/orders/{id}`, and cancellation is represented as `/orders/{id}/cancellation`.

## A4. Resource Table

| Method | URL | What it does | Success code | Failure codes |
|---|---|---|---|---|
| POST | `/orders` | Creates a new order after validating the request and successfully processing payment | 201 Created + Location | 400, 409, 422, 503 |
| GET | `/orders/{id}` | Retrieves one order by its order ID | 200 OK | 404 |
| GET | `/orders?status={status}` | Returns orders filtered by their current status | 200 OK | 400 |
| POST | `/orders/{id}/cancellation` | Changes an existing cancellable order to `CANCELLED` | 200 OK | 404, 409 |

## A5. Awkward Resource Mapping

Cancellation is the operation that maps least comfortably from the SOAP-style operation `cancelOrder(orderId)`. A generic alternative would be `PATCH /orders/{id}` with `{"status":"CANCELLED"}`, but that would expose arbitrary lifecycle-state modification. A verb-style endpoint such as `POST /cancelOrder` was also rejected because it is less resource-oriented and does not identify the order in the URL. The selected design, `POST /orders/{id}/cancellation`, treats cancellation as a state-changing sub-resource while keeping it explicitly associated with one order.

---

# 2. Part B — OpenAPI Contract

The OpenAPI contract was written before the implementation handlers. It defines the service metadata, server, four required endpoints, reusable schemas, request parameters, request bodies, success responses, and failure responses.

The contract uses **OpenAPI 3.0.3**.

## OpenAPI Endpoints

```text
POST /orders
GET /orders/{id}
GET /orders?status={status}
POST /orders/{id}/cancellation
```

Schemas are declared once under `components.schemas` and reused with `$ref`.

The main schemas are:

- `CreateOrderRequest`
- `OrderItemRequest`
- `OrderResponse`
- `OrderItemResponse`
- `OrderStatus`
- `Problem`

Every failure uses the same problem representation containing:

```json
{
  "type": "...",
  "title": "...",
  "status": 400,
  "detail": "..."
}
```

## OpenAPI Validation

Command used:

```text
python -m openapi_spec_validator openapi.yaml
```

Result:

```text
openapi.yaml: OK
```

**Line counts for Question 1:**

- Assignment 3 `partner.wsdl`: **70 lines**
- Final Assignment 4 `openapi.yaml`: **303 lines**

The difference is explained by the fact that the two contracts describe different service styles and therefore need different amounts of structural metadata.

---

# 3. Part C — Implementation

## C1. Service Layout

The service follows the required Tutorial 4-style structure:

```text
assignment-4/
└── orders/
    ├── openapi.yaml
    ├── app.py
    ├── models.py
    ├── store.py
    ├── errors.py
    ├── payment_client.py
    ├── mock_payments.py
    ├── NOTES.md
    └── tests/
        ├── conftest.py
        └── test_orders.py
```

Storage is implemented using an in-process dictionary. The Orders Service owns this store; the Payments mock is accessed through HTTP and does not import the Orders store.

## C2. Record vs Representation

The `Order` model stores Python attributes such as:

```text
order_id
student_id
address_id
items
total
status
```

The model's `as_json()` method produces the published representation using API field names such as `orderId`, `studentId`, and `addressId`.

Therefore the stored record and the public representation are not identical. Internal Python attribute naming is not exposed directly.

No credentials or internal implementation-only data are returned.

## C3. Four Required Endpoints

The implementation provides:

```text
POST /orders
GET /orders/{id}
GET /orders?status={status}
POST /orders/{id}/cancellation
```

The four endpoints also appear in `openapi.yaml`.

## C4. Request Validation

A dedicated:

```python
validate(data)
```

function validates the create-order request before the handler uses individual request-body fields.

It checks:

- the request body is a JSON object;
- required fields are present;
- `items` is a non-empty list;
- every item is an object;
- every item contains `itemId` and `quantity`;
- quantity is an integer;
- quantity is at least 1.

For example, syntactically valid JSON with a quantity of `0` would otherwise reach the order-processing logic, but `validate()` rejects it with `422 Unprocessable Content`.

## C5. HTTP Status Codes

The service uses status codes according to the assignment:

- **201 Created** + `Location` on successful creation.
- **200 OK** for successful reads and cancellation.
- **400 Bad Request** for malformed JSON or invalid request/query syntax.
- **404 Not Found** for an unknown order.
- **409 Conflict** for an invalid state transition or idempotency-key conflict.
- **422 Unprocessable Content** when the request is syntactically valid but rejected by a business/domain rule.
- **503 Service Unavailable** when the Payments dependency remains unavailable after retries.

## C6. Single Error Shape

All service errors use the single:

```python
problem(status, title, detail, problem_type=None)
```

helper.

The published error fields are:

```text
type
title
status
detail
```

Endpoints do not invent separate error formats.

## C7. Safe Retry / Idempotency

Order creation is the endpoint where duplicate work could cause real damage, particularly because it involves payment.

The client supplies:

```text
Idempotency-Key
```

The key and original request/response are stored by the service.

When the same key is submitted again with the same request body, the original response is returned without creating another order or repeating the payment operation.

If the same key is reused with a different request body, the service returns:

```text
409 Conflict
```

This prevents one idempotency key from representing two different operations.

## C8. Automated Tests

The test suite contains seven tests covering:

1. successful order creation;
2. idempotent repeat;
3. idempotency-key conflict;
4. unknown order;
5. payment failure fallback;
6. invalid quantity;
7. invalid status filter.

Final test result:

```text
pytest -q

7 passed in 0.23s
```

---

# 4. Part D — Surviving the Network

## D1. Cross-Service HTTP Call

The Orders Service makes a real HTTP request to the Payments Service.

The Payments Service address is resolved from:

```text
PAYMENTS_URL
```

It is not hard-coded in the client.

Example local configuration:

```powershell
$env:PAYMENTS_URL="http://127.0.0.1:5001/payments/charge"
```

The Orders Service sends the payment request using HTTP POST and includes the same `Idempotency-Key` received for the order creation.

## D2. Timeout and Retry

The outbound Payments call uses:

```text
Connection timeout: 2 seconds
Read timeout: 3 seconds
Maximum total attempts: 3
Base backoff: 0.2 seconds
```

Retries occur for:

- network connection failures;
- connection/read timeouts;
- HTTP 5xx responses.

HTTP 4xx responses are **not retried**.

The retry delay uses exponential backoff:

```text
0.2 × 2^(attempt - 1)
```

with random jitter added to the delay.

Because order creation is retried, the `Idempotency-Key` is forwarded on every outbound payment attempt.

## D3. Fallback Decision

The service uses a **fail-closed** payment policy. If Payments remains unreachable, times out, or returns 5xx after all retry attempts, Orders returns `503 Service Unavailable` and does not create the order. Degrading by creating an unpaid order would be incorrect because the client could receive a successful-looking order even though payment was never confirmed.

If Payments returns a 4xx response, the request is not retried and the payment failure is mapped to `422 Unprocessable Content`.

---

# 5. Curl Transcript

The following transcript demonstrates the minimum evidence requested by the assignment.

## 5.1 Successful Create — 201 + Location

Command:

```powershell
curl.exe -i -X POST "http://127.0.0.1:5000/orders" -H "Content-Type: application/json" -H "Idempotency-Key: curl-create-001" --data-binary "@curl-order.json"
```

Output:

```text
HTTP/1.1 201 CREATED
Server: Werkzeug/3.1.8 Python/3.11.9
Content-Type: application/json
Location: /orders/ORD-1001
Connection: close

{
  "addressId": "ADDR-CURL-001",
  "items": [
    {
      "itemId": "ITEM-101",
      "price": 249.5,
      "quantity": 2
    }
  ],
  "orderId": "ORD-1001",
  "status": "PLACED",
  "studentId": "STU-CURL-001",
  "total": 499.0
}
```

## 5.2 Same Request — Idempotent Repeat

The same request was repeated using the same:

```text
Idempotency-Key: curl-create-001
```

Output:

```text
HTTP/1.1 201 CREATED
Server: Werkzeug/3.1.8 Python/3.11.9
Content-Type: application/json
Location: /orders/ORD-1001
Connection: close

{
  "addressId": "ADDR-CURL-001",
  "items": [
    {
      "itemId": "ITEM-101",
      "price": 249.5,
      "quantity": 2
    }
  ],
  "orderId": "ORD-1001",
  "status": "PLACED",
  "studentId": "STU-CURL-001",
  "total": 499.0
}
```

The same `ORD-1001` was returned instead of creating a second order.

## 5.3 Malformed JSON — 400

```text
HTTP/1.1 400 BAD REQUEST
Server: Werkzeug/3.1.8 Python/3.11.9
Content-Type: application/json
Connection: close

{
  "detail": "Request body must contain valid JSON.",
  "status": 400,
  "title": "Malformed request body",
  "type": "https://api.campuseats.example.com/problems/malformed-request-body"
}
```

## 5.4 Missing Resource — 404

Command:

```powershell
curl.exe -i -X GET "http://127.0.0.1:5000/orders/ORD-9999"
```

Output:

```text
HTTP/1.1 404 NOT FOUND
Server: Werkzeug/3.1.8 Python/3.11.9
Content-Type: application/json
Connection: close

{
  "detail": "No order exists with id ORD-9999.",
  "status": 404,
  "title": "Order not found",
  "type": "https://api.campuseats.example.com/problems/order-not-found"
}
```

## 5.5 State Conflict — 409

The order `ORD-1001` had already been cancelled. Repeating the cancellation produced:

```text
HTTP/1.1 409 CONFLICT
Server: Werkzeug/3.1.8 Python/3.11.9
Content-Type: application/json
Connection: close

{
  "detail": "Order ORD-1001 cannot be cancelled from status CANCELLED.",
  "status": 409,
  "title": "Order cannot be cancelled",
  "type": "https://api.campuseats.example.com/problems/order-cannot-be-cancelled"
}
```

---

# 6. Required Answers

## Answer 1 — WSDL Lines vs OpenAPI Lines

The Assignment 3 `partner.wsdl` contains **70 lines**, while the final Assignment 4 `openapi.yaml` contains **303 lines**. The difference is not simply unused text.

WSDL is an XML contract that explicitly describes XML data types, messages, operations, SOAP binding details, and the service/port endpoint. OpenAPI expresses the REST contract mainly through paths, HTTP methods, parameters/request bodies, responses, and reusable schemas.

Two things explicitly declared by the WSDL that the OpenAPI file does not need are:

1. **SOAP binding / SOAPAction details**, because REST uses HTTP methods and resource URLs rather than SOAP envelopes and SOAPAction.
2. **WSDL message/port/service structure**, because OpenAPI directly describes HTTP requests and responses and does not need separate SOAP `message`, `portType`, `binding`, and `service/port` declarations.

## Answer 2 — SOAP Fault to HTTP Problem

One SOAP Fault from Assignment 3 was:

```xml
<soap:Fault>
  <faultcode>soap:Client</faultcode>
  <faultstring>Payment declined</faultstring>
  <detail>
    <pay:PaymentError>
      <pay:code>card_declined</pay:code>
      <pay:message>
        The payment instrument was declined.
      </pay:message>
    </pay:PaymentError>
  </detail>
</soap:Fault>
```

The REST version maps this to an HTTP failure:

```text
HTTP/1.1 422 UNPROCESSABLE CONTENT
```

with a problem body such as:

```json
{
  "type": "https://api.campuseats.example.com/problems/payment-declined",
  "title": "Payment declined",
  "status": 422,
  "detail": "Payments Service returned 400"
}
```

Returning an application error inside `200 OK` is a problem because network components, clients, monitoring systems, caches, and retry logic normally interpret the HTTP status code first. A `200` says the operation succeeded, so an intermediary may record or treat the response as successful even though the application operation failed. Using `4xx`/`5xx` makes the failure visible at the HTTP/network boundary.

## Answer 3 — UDDI Publish / Find / Bind

The traditional UDDI-style flow can be understood as:

- **Publish:** a service provider publishes its service information.
- **Find:** a consumer searches the registry for a suitable service.
- **Bind:** the consumer obtains the contract and endpoint information and uses it to call the service.

In the Assignment 3 design, the live UDDI server was replaced by a modern service catalogue/registry entry and/or a direct WSDL URL. Therefore the same conceptual publish/find/bind activities remain, but the centralized UDDI mechanism disappeared. The service catalogue/registry and direct contract URL take over discovery, while the WSDL still supplies the SOAP contract at the external partner boundary.

## Answer 4 — XML Schema vs `validate()`

In Assignment 3, the XML Schema described the expected structure and data types of the SOAP request. In the REST implementation, the equivalent application-level check is the Python:

```python
validate(data)
```

function in `app.py`.

For example, JSON containing:

```json
{
  "studentId": "STU-001",
  "addressId": "ADDR-001",
  "items": [
    {
      "itemId": "ITEM-101",
      "quantity": 0
    }
  ]
}
```

is syntactically valid JSON, but the domain rejects it because quantity must be at least 1. Without `validate()`, this invalid value could reach the order-processing logic.

## Answer 5 — Where SOAP Is Still Preferable

SOAP is still preferable at a strict enterprise integration boundary where a formal WSDL contract, message-level security, standardized SOAP faults, and WS-* style enterprise features are required. The exact guarantee purchased is a strongly defined contract and message-processing model that is standardized beyond the basic HTTP request/response semantics of REST. This is why Assignment 3 kept SOAP specifically at the external payment-partner boundary while the internal CampusEats APIs use REST.

---

# 7. Final Verification

## OpenAPI

```text
python -m openapi_spec_validator openapi.yaml

openapi.yaml: OK
```

## Automated Tests

```text
pytest -q

7 passed in 0.23s
```

## Required Curl Evidence

- Successful create → **201 Created + Location** ✓
- Same request with same idempotency key → **original order returned** ✓
- Malformed request body → **400 Bad Request** ✓
- Missing resource → **404 Not Found** ✓
- State conflict → **409 Conflict** ✓

## Submission Files

Submit the complete:

```text
assignment-4/orders/
```

folder containing:

```text
openapi.yaml
app.py
models.py
store.py
errors.py
payment_client.py
mock_payments.py
NOTES.md
tests/
```

Do not include unnecessary generated folders such as `__pycache__` or `.pytest_cache` unless specifically required.
