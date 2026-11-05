# CampusEats – REST API

**Course:** CS543 – Web Services  
**Assignment:** 8  
**Project:** CampusEats – Food Menu Management Service

## 1. Project Overview

CampusEats is a simple food menu management application developed using Node.js and Express.js.

It provides REST API endpoints to retrieve all food items, view individual items, and add new dishes. A simple frontend allows users to view the menu and add new dishes with their price and availability status.

The application uses an in-memory JavaScript array to store food items.

## 2. Team Members

| S. No. | Name | Roll Number |
|---|---|---|
| 1 | Mahi Verma | 20252651032 |
| 2 | Subham Kumar Mohanty | 20252651057 |
| 3 | Abhishek Jadhao | 20252651003 |
| 4 | Harsh N Shende | 20252651023 |
| 5 | Rishabh Mishra | 20252651041 |

## 3. Technologies Used

- Node.js
- Express.js
- HTML
- CSS
- JavaScript
- REST API
- Fetch API

## 4. API Endpoints

The application provides the following REST API endpoints:

| HTTP Method | Endpoint | Description |
|---|---|---|
| GET | `/items` | Retrieve all food items |
| GET | `/items/:id` | Retrieve a specific food item by ID |
| POST | `/items` | Add a new food item |

### Example: GET /items

Retrieves all food items.

### Example: GET /items/1

Retrieves the food item with ID 1.

### Example: POST /items

Adds a new food item.

**Sample JSON Request:**

```json
{
  "name": "Chicken Roll",
  "price": 120,
  "available": true
}
```

## 5. HTTP Status Codes

| Status Code | Description |
|---|---|
| 200 OK | Request completed successfully |
| 201 Created | New food item successfully created |
| 404 Not Found | Requested food item does not exist |
| 422 Unprocessable Entity | Required field is missing |

## 6. Request Handling

### req.params

`req.params.id` is used in the `GET /items/:id` endpoint to retrieve the ID of a food item from the URL.

### req.body

`req.body` is used in the `POST /items` endpoint to access the data sent by the client when adding a new food item.

### express.json()

`express.json()` is middleware used to parse incoming JSON request bodies. It allows the application to access the submitted JSON data through `req.body`.

## 7. Frontend Features

The frontend provides the following features:

- Display all food items.
- Show the price of each dish.
- Display whether a dish is Available or Unavailable.
- Add new food items through a form.
- Select the availability status while adding a dish.
- Automatically refresh the menu after adding a new dish.

The frontend communicates with the backend using JavaScript's Fetch API.

## 8. Data Storage

The application uses an in-memory JavaScript array to store food items.

Four sample food items are available when the server starts.

New food items can be added through the frontend or by sending POST requests to the API.

**Note:** Since the application uses in-memory storage, newly added data is lost when the server restarts.

## 9. Project Structure

```text
CampusEats_Assignment8/
│
├── server.js
├── package.json
├── package-lock.json
├── README.md
│
└── public/
    ├── index.html
    └── style.css
```

## 10. How to Run the Project

Follow these steps to run the application locally.

**Step 1: Clone the repository**

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

**Step 2: Navigate to the project folder**

```bash
cd CampusEats_Assignment8
```

**Step 3: Install dependencies**

```bash
npm install
```

**Step 4: Start the server**

```bash
node server.js
```

**Step 5: Open the application**

Open the following URL in your browser:

```text
http://localhost:3000
```

## 11. GitHub Repository

**Repository Link:** https://github.com/subhamohanty07/campuseats.git

## 12. Conclusion

CampusEats demonstrates the implementation of a simple RESTful web service using Node.js and Express.js. It covers the basic concepts of REST API development, HTTP methods, request handling, status codes, JSON data exchange, and frontend-backend communication using the Fetch API.