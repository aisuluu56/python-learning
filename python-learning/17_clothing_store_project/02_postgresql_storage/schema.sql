-- Этап 02. SQL-схема проекта
-- Таблицы для интернет-магазина одежды

-- Таблица категорий
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

-- Таблица товаров
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    name TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    color TEXT NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

-- Таблица остатков товаров по размерам
CREATE TABLE IF NOT EXISTS product_stocks (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    size TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    UNIQUE(product_id, size)
);

-- Таблица покупателей
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL
);

-- Таблица заказов
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'new',
    total_amount DECIMAL(12,2) NOT NULL
);

-- Таблица позиций заказа
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    size TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price_at_moment DECIMAL(10,2) NOT NULL
);

-- Таблица адресов доставки
CREATE TABLE IF NOT EXISTS delivery_addresses (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    postal_code TEXT,
    is_default BOOLEAN DEFAULT FALSE
);