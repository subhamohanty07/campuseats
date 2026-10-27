# CampusEats — GraphQL Menu Service

## 1. Project Overview

CampusEats is a web-based food menu management service developed using GraphQL, Node.js, Express, and MySQL. It allows users to view menu items and add new dishes through a simple web interface.

The application uses GraphQL queries to retrieve menu data and a GraphQL mutation to insert new dishes into the MySQL database.

## 2. Team Members

Add the team members' names and roll numbers required for your assignment here.

| Name | Roll Number |
|---|---|
| Subham Kumar Mohanty | 20252651057 |
| Mahi Verma | 20252651032 |
| Rishabh  Mishra | 20252651041 |
| Abhishek Jadhao | 20252651003 |
| Harsh N Shende | 20252651023 |

## 3. Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Node.js, Express.js
- **API:** GraphQL, Apollo Server
- **Database:** MySQL
- **Database Driver:** mysql2
- **Development Tool:** Visual Studio Code

## 4. Features

- Display all menu dishes from MySQL.
- Retrieve individual dishes by ID through GraphQL.
- Add a new dish using a GraphQL mutation.
- Store dish names, prices, and availability in MySQL.
- Automatically refresh the menu after adding a dish.
- Display dish availability in the user interface.

## 5. Project Structure

```text
CampusEats_Assignmentt7/
├── public/
│   └── index.html
├── db.js
├── schema.graphql
├── schema.sql
├── server.js
├── package.json
├── package-lock.json
├── .env
└── .gitignore
```

**Note:** The `.env` file contains local database credentials and must not be uploaded to GitHub.

## 6. Database Setup

The application uses a MySQL database named `campuseats_graphql`.

The `dishes` table contains the following fields:

| Field | Description |
|---|---|
| `id` | Unique dish identifier |
| `name` | Name of the dish |
| `price` | Price of the dish |
| `available` | Whether the dish is available |

To create the table and insert the initial sample data, run:

```powershell
Get-Content .\schema.sql | mysql -u root -p campuseats_graphql
```

Configure the database credentials in the local `.env` file.

## 7. Installation and Execution

### Install dependencies

```powershell
npm install
```

### Configure environment variables

Create a `.env` file in the project root:

```dotenv
DB_HOST=localhost
DB_USER=campuseats_app
DB_PASSWORD=YOUR_LOCAL_DATABASE_PASSWORD
DB_NAME=campuseats_graphql
```

Replace the placeholder with the local database password configured for `campuseats_app`.

### Start the server

```powershell
npm start
```

Open the application at:

`http://localhost:4000`

The GraphQL endpoint is:

`http://localhost:4000/graphql`

## 8. GraphQL Operations

### Query: Retrieve all dishes

```graphql
query {
  dishes {
    id
    name
    price
    available
  }
}
```

### Query: Retrieve one dish

```graphql
query {
  dish(id: 1) {
    id
    name
    price
    available
  }
}
```

### Mutation: Add a dish

```graphql
mutation {
  addDish(input: {
    name: "Paneer Sandwich"
    price: 80
    available: true
  }) {
    id
    name
    price
    available
  }
}
```

## 9. Assignment Questions

### Q1. Which CampusEats service did you choose?

We selected the **Menu/Dishes Service**. It manages menu information and provides GraphQL operations to retrieve dishes and add new dishes.

### Q2. Name one field a client can skip and one it cannot. Why use `!`?

The `available` field in `AddDishInput` is optional because it does not use `!`. A client can omit it when adding a dish, and the resolver defaults it to `true`.

The `name` field is required because it is declared as `String!`. The exclamation mark means that the value cannot be `null`. Similarly, `AddDishInput!` requires the mutation to receive an input object.

### Q3. Map GraphQL to SQL: which part of the query became WHERE, and which resolver ran INSERT?

In the `dish(id: ID!)` query, the requested `id` becomes the parameter in the SQL condition:

```sql
SELECT id, name, price, available
FROM dishes
WHERE id = ?;
```

The `?` is replaced with the supplied ID using a parameterized query.

The `addDish` mutation resolver executes:

```sql
INSERT INTO dishes (name, price, available)
VALUES (?, ?, ?);
```

This inserts the new dish into MySQL.

## 10. Testing

The following operations were tested during development:

- Loading all dishes from the database.
- Displaying available and unavailable menu items.
- Adding a new dish through the web interface.
- Refreshing the menu after a successful mutation.
- Verifying inserted records in MySQL.

## 11. Submission Links

- **GitHub Repository:** Add your repository URL here.
- **Google Drive Demo Video:** Add your demo video link here.
- **Screenshots:** Add the before-and-after screenshots required for the assignment.
