-- Pay for Tools Database Schema
-- SQLite Database Structure

-- Expenses table
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    merchant_name TEXT NOT NULL,
    amount REAL NOT NULL,
    pay_time TEXT NOT NULL,
    product_description TEXT,
    order_no TEXT,
    category TEXT DEFAULT '其他',
    remark TEXT,
    screenshot_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SQLite internal sequence table (auto-generated)
-- CREATE TABLE sqlite_sequence(name,seq);
