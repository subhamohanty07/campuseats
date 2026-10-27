
require("dotenv").config();

const fs = require("fs");
const path = require("path");
const express = require("express");
const cors = require("cors");
const { ApolloServer } = require("@apollo/server");
const { expressMiddleware } = require("@as-integrations/express5");
const pool = require("./db");

const app = express();
const PORT = 4000;

const typeDefs = fs.readFileSync(
  path.join(__dirname, "schema.graphql"),
  "utf8"
);

const resolvers = {
  Query: {
    dishes: async () => {
      const [rows] = await pool.query(
        "SELECT id, name, price, available FROM dishes ORDER BY id"
      );
      return rows.map((dish) => ({
        ...dish,
        price: Number(dish.price),
        available: Boolean(dish.available)
      }));
    },

    dish: async (_, { id }) => {
      const [rows] = await pool.execute(
        "SELECT id, name, price, available FROM dishes WHERE id = ?",
        [id]
      );

      if (rows.length === 0) {
        return null;
      }

      return {
        ...rows[0],
        price: Number(rows[0].price),
        available: Boolean(rows[0].available)
      };
    }
  },

  Mutation: {
    addDish: async (_, { input }) => {
      const { name, price, available = true } = input;

      const [result] = await pool.execute(
        "INSERT INTO dishes (name, price, available) VALUES (?, ?, ?)",
        [name, price, available]
      );

      const [rows] = await pool.execute(
        "SELECT id, name, price, available FROM dishes WHERE id = ?",
        [result.insertId]
      );

      return {
        ...rows[0],
        price: Number(rows[0].price),
        available: Boolean(rows[0].available)
      };
    }
  }
};

async function startServer() {
  const server = new ApolloServer({
    typeDefs,
    resolvers
  });

  await server.start();

  app.use(cors());
  app.use(express.json());

  app.use(
    "/graphql",
    expressMiddleware(server)
  );

  app.use(express.static(path.join(__dirname, "public")));

  app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "index.html"));
  });

  app.listen(PORT, () => {
    console.log(`CampusEats server running at http://localhost:${PORT}`);
    console.log(`GraphQL endpoint: http://localhost:${PORT}/graphql`);
  });
}

startServer().catch((error) => {
  console.error("Failed to start server:", error);
  process.exit(1);
});
