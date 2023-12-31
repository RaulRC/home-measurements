CREATE TABLE IF NOT EXISTS measurements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    place VARCHAR(255) NOT NULL,
    room VARCHAR(255) NOT NULL,
    timestamp DATETIME,
    temperature FLOAT,
    humidity FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)  ENGINE=INNODB;

-- PG
CREATE TABLE IF NOT EXISTS measurements (
    id SERIAL,
    place VARCHAR(255) NOT NULL,
    room VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP,
    key VARCHAR(255),
    value FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
