DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

DROP TABLE IF EXISTS comments;

CREATE TABLE comments (
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    post_id INTEGER NOT NULL,
    content TEXT NOT NULL
);

DROP TABLE IF EXISTS email_ids_subscriptions;

CREATE TABLE email_ids (
    email_ids_subscriptions TEXT PRIMARY KEY
)

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    email_id TEXT PRIMARY KEY
    pass_key TEXT 
)