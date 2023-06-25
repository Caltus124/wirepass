CREATE TABLE IF NOT EXISTS users (
    _id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(50),
    source_ip VARCHAR(50),
    destination_ip VARCHAR(50),
    username VARCHAR(255),
    password VARCHAR(255),
    day VARCHAR(255),
    heur VARCHAR(255)
)

INSERT INTO users (type, source_ip, destination_ip, username, password, day, heur)
VALUES
    ('FTP', '192.168.1.100', '10.0.0.1', 'user1', 'password1', '2023-06-25', '08:00:00'),
    ('SMTP', '192.168.1.200', '10.0.0.2', 'user2', 'password2', '2023-06-25', '09:30:00'),
    ('LDAP', '192.168.1.150', '10.0.0.3', 'user3', 'password3', '2023-06-25', '11:15:00'),
    ('FTP', '192.168.1.120', '10.0.0.4', 'user4', 'password4', '2023-06-25', '13:45:00'),
    ('SMTP', '192.168.1.180', '10.0.0.5', 'user5', 'password5', '2023-06-25', '15:20:00');
