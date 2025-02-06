CREATE TABLE teacher_entity (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    sub_id INT,
    address VARCHAR(255),
    age INT,
    exp INT,
    qualification VARCHAR(255),
    password VARCHAR(255)
);