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


Port	            Service	            Name

tcp/20, tcp/21	    FTP	        YES     File Transfer Protocol                  
tcp/23	            Telnet	            Teletype Network Protocol
tcp/25	            SMTP	            Simple Mail Transfer Protocol
tcp/80	            HTTP	            Hyper Text Transfer Protocol
tcp/110	            POP3	            Post Office Protocol
tcp/143	            IMAP4	            Internet Message Access Protocol
udp/161, udp/162	SNMP	            Simple Network Management Protocol
tcp/389	            LDAP	            Lightweight Directory Access Protocol
tcp/1080	        SOCKS	            SOCKetS Proxy Protocol
tcp/1433	        MSSQL	            Microsoft SQL Database
tcp/5222	        XMPP	            Extensible Messaging and Presence Protocol (Jabber)
tcp/5432	        PostgreSQL	        PostgreSQL Database
tcp/6667	        IRC	                Internet Relay Chat
                    OSPF                Open Shortest Path First
                    BFD                 Bidirectional Forwarding Detection
                    STUN                Session Traversal Utilities for NAT 
                    DNS                 Domain Name System
                    TFTP                Trivial File Transfer Protocol
                    SIP                 Session Initiation Protocol
                    RDP                 Remote Desktop Protocol