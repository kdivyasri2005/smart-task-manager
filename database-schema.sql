CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(200)
);

CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    description TEXT,
    priority VARCHAR(20),
    status VARCHAR(20),
    created_date TIMESTAMP,
    user_id INTEGER REFERENCES users(id)
);