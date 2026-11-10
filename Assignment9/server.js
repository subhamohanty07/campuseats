
require('dotenv').config();

const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

const app = express();
const PORT = 3000;
const SECRET = process.env.JWT_SECRET;

if (!SECRET) {
    console.error('Error: JWT_SECRET is missing. Add it to your .env file.');
    process.exit(1);
}

app.use(express.json());
app.use(express.static('public'));


// Users with hashed passwords
const users = [
    {
        id: 1,
        username: 'subham',
        password: bcrypt.hashSync('subham123', 10),
        role: 'customer'
    },
    {
        id: 2,
        username: 'subhsrestaurant',
        password: bcrypt.hashSync('subhsrestaurant123', 10),
        role: 'restaurant'
    }
];


// Existing menu items
let items = [
    { id: 1, name: 'Veg Burger', price: 60, available: true },
    { id: 2, name: 'Paneer Roll', price: 90, available: true },
    { id: 3, name: 'Masala Dosa', price: 70, available: true },
    { id: 4, name: 'French Fries', price: 50, available: false }
];

let nextId = 5;


// Login route
app.post('/login', (req, res) => {
    const { username, password } = req.body;

    const user = users.find(u => u.username === username);

    if (!user || !password || !bcrypt.compareSync(password, user.password)) {
        return res.status(401).json({
            error: 'Invalid username or password'
        });
    }

    const token = jwt.sign(
        { id: user.id, role: user.role },
        SECRET,
        { expiresIn: '1h' }
    );

    res.json({
        message: 'Login successful',
        token,
        role: user.role
    });
});


// Authentication middleware
function auth(req, res, next) {
    const authHeader = req.get('Authorization') || '';

    const token = authHeader.startsWith('Bearer ')
        ? authHeader.split(' ')[1]
        : null;

    if (!token) {
        return res.status(401).json({
            error: 'Access denied. Token required.'
        });
    }

    try {
        req.user = jwt.verify(token, SECRET);
        next();
    } catch (error) {
        return res.status(401).json({
            error: 'Invalid or expired token'
        });
    }
}


// Authorization middleware
const requireRole = (...allowedRoles) => (req, res, next) => {
    if (!allowedRoles.includes(req.user.role)) {
        return res.status(403).json({
            error: 'Forbidden: insufficient permissions'
        });
    }

    next();
};


// Get all items (authentication required)
app.get('/items', auth, (req, res) => {
    res.json(items);
});


// Get item by ID (authentication required)
app.get('/items/:id', auth, (req, res) => {
    const item = items.find(i => i.id === Number(req.params.id));

    if (!item) {
        return res.status(404).json({
            error: 'Item not found'
        });
    }

    res.json(item);
});


// Add new item (restaurant/admin role required)
app.post('/items', auth, requireRole('restaurant', 'admin'), (req, res) => {
    const { name, price, available } = req.body;

    if (!name) {
        return res.status(422).json({
            error: 'Name is required'
        });
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
app.listen(PORT, () => {
    console.log(`CampusEats running at http://localhost:${PORT}`);
});
