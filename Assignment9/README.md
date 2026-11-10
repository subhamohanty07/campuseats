# CampusEats – Assignment 09: Securing the API

**Course:** CS543 – Web Services

This project continues the CampusEats REST service from Assignment 08. It keeps the same menu data and routes and adds JWT authentication and role-based authorization.

## Team members

| No. | Name | Roll Number |
|---|---|---|
| 1 | Mahi Verma | 20252651032 |
| 2 | Subham Kumar Mohanty | 20252651057 |
| 3 | Abhishek Jadhao | 20252651003 |
| 4 | Harsh N Shende | 20252651023 |
| 5 | Rishabh Mishra | 20252651041 |

## Demo video and screenshots

Google Drive link: <https://drive.google.com/file/d/1TOEHGjmVwGZTmJWoxJEcZDQK8pPuhOyf/view?usp=drive_link>

The demo shows the five cases: 401, login with token, 200, 201 and 403.

## Requirements

- Node.js and npm
- VS Code or another code editor

## Setup

1. Open this project folder in VS Code.
2. Install the dependencies:

   ```bash
   npm install
   ```

3. Create a file named `.env` in the project root. Copy the content from `.env.example` and provide a long secret value:

   ```env
   JWT_SECRET=replace_this_with_a_long_random_secret
   ```

   Do not upload `.env` to GitHub. It is already listed in `.gitignore`.

4. Start the server:

   ```bash
   npm start
   ```

5. Open <http://localhost:3000> in your browser.

## Demo accounts

The server creates two demo users. Passwords are converted to bcrypt hashes when the server starts; plain-text passwords are not stored in the user records.

| Username | Password | Role |
|---|---|---|
| `subham` | `subham123` | customer |
| `subhsrestaurant` | `subhsrestaurant123` | restaurant |

The login endpoint returns a JWT that expires after one hour.

## Routes and permissions

| Method | Path | Access |
|---|---|---|
| POST | `/login` | Public; used to obtain a token |
| GET | `/items` | Any authenticated user |
| GET | `/items/:id` | Any authenticated user |
| POST | `/items` | Authenticated `restaurant` or `admin` role |

## Frontend

The `public/` folder has a simple web page for the API. Users can log in, search and filter the menu, and add dishes to a cart. Restaurant users also see a form to add a new dish. The page only hides the form for customers. The real protection is on the server, which returns 403 if a customer tries to add a dish.

## README assignment questions

**1. Which routes require only authentication, and which also require a role?**

- `GET /items` – requires authentication only; any logged-in user can read the menu.
- `GET /items/:id` – requires authentication only; any logged-in user can read one dish.
- `POST /items` – requires authentication and the `restaurant` or `admin` role to add a dish.
- `POST /login` – public route; users use it to log in and receive a token.

**2. Show one 401 and one 403 from your demo. Why did the server return each code?**

- `401 Unauthorized` – the request to `GET /items` had no token. It was 401, not 403, because the server did not know who the user was.
- `403 Forbidden` – the customer sent a valid token to `POST /items`. It was 403, not 401, because the server knew who the user was, but the `customer` role is not allowed to add menu items.

**3. What is inside your JWT payload? Why is it safe to trust the role claim on the server, and why must the secret stay out of your code?**

The payload contains the user's `id` and `role`. It also has `iat` (time issued) and `exp` (expiry time) that the library adds. The server verifies the JWT signature with `jwt.verify` before using these claims. If a user changes the role in the token, the signature no longer matches, so the server rejects it. This is why the role claim is safe to trust. The JWT secret must stay outside the source code so it is not exposed when the project is shared or uploaded to GitHub. Anyone who knows the secret can create a fake token with any role.

## Testing with curl

Run these commands in a terminal while the server is running. They assume the default port `3000`. These examples use bash-style quotes. In Windows PowerShell, use `curl.exe` instead of `curl`.

### 1. Request without a token – expect 401

```bash
curl -i http://localhost:3000/items
```

### 2. Login as customer – copy the returned token

```bash
curl -X POST http://localhost:3000/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"subham\",\"password\":\"subham123\"}"
```

### 3. Use the customer token to read menu – expect 200

Replace `CUSTOMER_TOKEN` with the token returned by login:

```bash
curl -i http://localhost:3000/items \
  -H "Authorization: Bearer CUSTOMER_TOKEN"
```

### 4. Login as restaurant – copy the returned token

```bash
curl -X POST http://localhost:3000/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"subhsrestaurant\",\"password\":\"subhsrestaurant123\"}"
```

Use the restaurant token to add a dish – expect 201:

```bash
curl -i -X POST http://localhost:3000/items \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer RESTAURANT_TOKEN" \
  -d "{\"name\":\"Veg Sandwich\",\"price\":80,\"available\":true}"
```

### 5. Try adding a dish with the customer token – expect 403

```bash
curl -i -X POST http://localhost:3000/items \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer CUSTOMER_TOKEN" \
  -d "{\"name\":\"Test Dish\",\"price\":50,\"available\":true}"
```