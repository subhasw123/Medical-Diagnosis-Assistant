CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    age TINYINT UNSIGNED NOT NULL,
    gender VARCHAR(30) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Run once on an existing database so diagnosis records can be scoped to users.
ALTER TABLE patients
    ADD COLUMN user_id INT NULL,
    ADD INDEX idx_patients_user_id (user_id),
    ADD CONSTRAINT fk_patients_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE SET NULL;
