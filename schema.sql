CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    shop VARCHAR(512),
    teatype VARCHAR(15),
    score INTEGER,
    reviewtext VARCHAR(601),
    picture_url VARCHAR(512),
    user_id INTEGER REFERENCES users
);
    
