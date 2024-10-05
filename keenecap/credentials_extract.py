from scapy.all import *
import re
from keenecap.logger import logger
import sys
# Regular expressions to extract cookies and Authorization headers

cookie_regex = re.compile(r'Cookie:\s*([^\r\n]+)', re.IGNORECASE)
auth_regex = re.compile(r'Authorization:\s*([^\r\n]+)', re.IGNORECASE)
host_regex = re.compile(r'Host:\s*([^\r\n]+)', re.IGNORECASE)
path_regex = re.compile(r'^(GET|POST)\s+([^\s]+)', re.IGNORECASE)

ftp_user_regex = re.compile(r'USER\s+([^\r\n]+)', re.IGNORECASE)
ftp_pass_regex = re.compile(r'PASS\s+([^\r\n]+)', re.IGNORECASE)

pop3_user_regex = re.compile(r'USER\s+([^\r\n]+)', re.IGNORECASE)
pop3_pass_regex = re.compile(r'PASS\s+([^\r\n]+)', re.IGNORECASE)

smtp_auth_regex = re.compile(r'AUTH\s+(PLAIN|LOGIN)\s+([^\r\n]+)', re.IGNORECASE)

# Function to analyze a packet and search for HTTP Cookie and Authorization headers
def extract_packet_info(packet):
    if packet.haslayer(TCP) and packet.haslayer(Raw):  # Check if it's a TCP packet with raw data
        try:
            
            has_match = False
            payload = packet[Raw].load.decode(errors='ignore')  # Extract raw data
            output = [] 
            
            ip_dst = packet[IP].dst if packet.haslayer(IP) else "N/A"
            port_dst = packet[TCP].dport
            
            output.append(f'DST IP: {ip_dst}')
            output.append(f'DST PORT: {port_dst}')
            # Extraction des informations HTTP
            cookies = cookie_regex.findall(payload)
            auth_headers = auth_regex.findall(payload)
            hosts = host_regex.findall(payload)
            paths = path_regex.findall(payload)

            if hosts:
                output.append(f'HOST: {hosts[0].strip()}')  # Display the host

            if paths:
                path = paths[0][1].strip()  
                output.append(f'PATH: {paths[0][1].strip()}')  # Display the path
                if path.__contains__('token') or path.__contains__('password'):
                    has_match = True

            if cookies:
                has_match = True
                output.append(f'COOKIES: {", ".join(cookies).strip()}')  # Display cookies

            if auth_headers:
                has_match = True
                output.append(f'AUTHORIZATION: {", ".join(auth_headers)}')  # Display Authorization header

            # Extract FTP credentials
            ftp_user = ftp_user_regex.findall(payload)
            ftp_pass = ftp_pass_regex.findall(payload)

            if ftp_user:
                has_match = True
                output.append(f'FTP USER: {ftp_user[0]}')
            if ftp_pass:
                has_match = True
                output.append(f'FTP PASS: {ftp_pass[0]}')

            # Extract POP3 credentials
            pop3_user = pop3_user_regex.findall(payload)
            pop3_pass = pop3_pass_regex.findall(payload)

            if pop3_user:
                has_match = True
                output.append(f'POP3 USER: {pop3_user[0]}')
            if pop3_pass:
                has_match = True
                output.append(f'POP3 PASS: {pop3_pass[0]}')

            # Extract SMTP credentials
            smtp_auth = smtp_auth_regex.findall(payload)

            if smtp_auth:
                has_match = True
                auth_type = smtp_auth[0][0]
                auth_creds = smtp_auth[0][1]
                output.append(f'SMTP AUTH ({auth_type}): {auth_creds}')

            # Display the result on a single line if information is found
            if output and has_match:
                logger.info(" | ".join(output).replace('\r', '').replace('\n', ''))

        except Exception as e:
            logger.error(f"Error analyzing packet: {e}")
def analyze_pcap_with_sniff(pcap_file, prefix='captures/'):
    logger.info(f"Analyzing pcap file: {pcap_file}")
    sniff(offline=prefix+pcap_file, session=TCPSession, prn=extract_packet_info)
    logger.info(f"pcap Analysis complete: {pcap_file}")


