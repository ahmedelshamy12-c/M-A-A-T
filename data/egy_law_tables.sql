CREATE TABLE users (
    id integer PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password  VARCHAR(255) NOT NULL,
    job VARCHAR(100),
    age integer,
    ssn VARCHAR(20) UNIQUE,
    role varchar(20) ,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE users;



CREATE TABLE Conversations (
    id integer PRIMARY KEY AUTOINCREMENT,
    user_id integer NOT NULL,
    title VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE Messages (
    id integer PRIMARY KEY AUTOINCREMENT,
    conversation_id integer,
    sender VARCHAR(50) NOT NULL,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (conversation_id) REFERENCES Conversations(id)
);
