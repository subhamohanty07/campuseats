
const express = require('express');
const app = express();

app.use(express.json());
app.use(express.static('public'));

// Initial menu data
let items = [
    { id: 1, name: 'Veg Burger', price: 60, available: true },
    { id: 2, name: 'Paneer Roll', price: 90, available: true },
    { id: 3, name: 'Masala Dosa', price: 70, available: true },
    { id: 4, name: 'French Fries', price: 50, available: false }
];

let nextId = 5;

// GET: Fetch all dishes
app.get('/items', (req, res) => {
    res.json(items);
});

// GET: Fetch one dish by ID
app.get('/items/:id', (req, res) => {
    const item = items.find(i => i.id === Number(req.params.id));

    if (!item) {
        return res.status(404).json({ error: 'Item not found' });
    }

    res.json(item);
});

// POST: Add a new dish
app.post('/items', (req, res) => {
    const { name, price, available } = req.body;

    if (!name) {
        return res.status(422).json({ error: 'Name is required' });
    }

    const newItem = {
        id: nextId++,
        name,
        price: Number(price) || 0,
        available: available !== false
    };

    items.push(newItem);

    res.status(201).json(newItem);
});

// Start server
app.listen(3000, () => {
    console.log('CampusEats running at http://localhost:3000');
});
