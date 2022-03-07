CREATE TABLE IF NOT EXISTS User (
    id INTEGER NOT NULL PRIMARY KEY, 
    name varchar(255),
    age int
);

CREATE TABLE IF NOT EXISTS Post (
    id INTEGER NOT NULL PRIMARY KEY,
    title varchar(255),
    content TEXT,

    user_id INTEGER NOT NULL,

    FOREIGN KEY (user_id) REFERENCES User(id)
);