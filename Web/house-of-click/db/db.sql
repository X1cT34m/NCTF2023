CREATE DATABASE web;
CREATE TABLE IF NOT EXISTS web.users (
    id Int32,
    username String,
    email String
) ENGINE = MergeTree()
ORDER BY id;
INSERT INTO web.users (id, username, email) VALUES (1, 'admin', 'admin'),(2, 'guest', 'guest');