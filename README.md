# CampusEats

CampusEats is a campus food ordering system developed as the running example for the Web Services course.

This repository contains the work completed for understanding HTTP communication, network analysis, service-oriented architecture, service boundaries, service contracts, database ownership, and inter-service communication.

---

## Team Members

| Team Member | Service |
|---|---|
| **Subham Kumar Mohanty** | Orders Service |
| **Mahi Verma** | Account Service |
| **Abhishek Jadhao** | Catalogue Service |
| **Harsh N Shende** | Payments & Delivery Service |
| **Rishabh Mishra** | Notification Service |

The project is developed collaboratively using Git and GitHub. Each team member works on a separate feature branch and contributes through pull requests.

---

## Project Architecture

CampusEats is divided into five services:

### 1. Account Service

**Owner:** Mahi Verma

Responsible for user and address management.

**Owns:**

- `users`
- `addresses`

### 2. Catalogue Service

**Owner:** Abhishek Jadhao

Responsible for restaurant and menu information.

**Owns:**

- `restaurants`
- `menu_items`

### 3. Orders Service

**Owner:** Subham Kumar Mohanty

Responsible for cart and order management.

**Owns:**

- `carts`
- `cart_items`
- `orders`
- `order_items`

### 4. Payments & Delivery Service

**Owner:** Harsh N Shende

Responsible for payment transactions, refunds, riders, and delivery assignments.

**Owns:**

- `transactions`
- `refunds`
- `riders`
- `assignments`

### 5. Notification Service

**Owner:** Rishabh Mishra

Responsible for managing notifications.

**Owns:**

- `message_log`

Each service owns its own data. No two services share the same database tables.

---

## Service Design

The CampusEats system follows the five main properties of a service:

1. **Reachable** — Each service can be accessed through defined operations.
2. **Self-contained** — Each service owns and manages its own data.
3. **Has a Contract** — Each service exposes defined operations that other services may call.
4. **Independent** — Services can be developed and changed independently.
5. **Loosely Coupled** — Services communicate through contracts rather than directly accessing each other's internal data.

---

## Service Contracts

Each service exposes operations through a defined contract.

The contract specifies:

- Operation name
- Input
- Output
- Possible errors

The internal database structure and implementation details are hidden from callers.

---

## Central Operation

The central business operation of CampusEats is:

```text
placeOrder