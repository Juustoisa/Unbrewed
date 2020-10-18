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
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    FOREIGN KEY (user_id) references users(id)
);
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    review_id INTEGER REFERENCES reviews ON DELETE CASCADE,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    commenttext VARCHAR(601),
    FOREIGN KEY (review_id) REFERENCES reviews(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE likes (
    review_id INTEGER REFERENCES reviews ON DELETE CASCADE,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    FOREIGN KEY (review_id) REFERENCES reviews(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    PRIMARY KEY(review_id, user_id)
);
