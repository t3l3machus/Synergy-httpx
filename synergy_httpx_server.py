#!/bin/python3
#
# Author by Panagiotis Chartas (t3l3machus)
# https://github.com/t3l3machus

from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl, sys, base64, re, os, argparse
from warnings import filterwarnings
from datetime import date, datetime
from urllib.parse import unquote, urlparse
from threading import Thread
from io import StringIO
from time import sleep
from subprocess import check_output

filterwarnings("ignore", category = DeprecationWarning)

''' Colors '''
MAIN = '\033[38;5;50m'
GREEN = '\033[38;5;82m'
BLUE = '\033[0;38;5;12m'
LPURPLE = '\033[0;38;5;201m'
ORANGE = '\033[0;38;5;214m'
ORANGEB = '\033[1;38;5;214m'
PURPLE = '\033[0;38;5;141m'
B_PURPLE = '\033[45m'
YELLOW="\033[0;38;5;11m"
RED = '\033[1;31m'
B_RED = '\033[41m'
END = '\033[0m'
B_END = '\033[49m'
BOLD = '\033[1m'
ULINE = '\033[4m'


''' MSG Prefixes '''
INFO = f'[{MAIN}Info{END}]'
WARN = f'[{ORANGE}Warning{END}]'
DBG = f'[{ORANGE}Debug{END}]'
IMPORTANT = f'[{ORANGE}Important{END}]'
FAILED = f'[{RED}Fail{END}]'

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cert", action="store", help = "Your certificate.")
parser.add_argument("-k", "--key", action="store", help = "The private key for your certificate. ")
parser.add_argument("-p", "--port", action="store", help = "Server port.", type = int)
parser.add_argument("-f", "--file", action="store", help = "File to be served via GET.")

args = parser.parse_args()



def print_green(msg):
	print(f'{GREEN}{msg}{END}')


def debug(msg):
	print(f'{DBG} {msg}{END}')


def chill():
	pass


# -------------- HTTPS Server -------------- #
class Https_Server(BaseHTTPRequestHandler):

	valid_endpoints = {
		'GET' : 'x3Rty7',
		'POST' : 'aWq8tY'
	}


	def do_GET(self):
		
		try:
			if self.path == f'/{self.valid_endpoints["GET"]}':
				self.server_version = "Apache/2.4.1"
				self.sys_version = ""
				self.send_response(200)
				self.send_header('Content-type', 'text/javascript; charset=UTF-8')
				self.send_header('Access-Control-Allow-Origin', '*')
				self.end_headers()
				
				try:
						print(f'GET {self.path} :\nFrom: {self.client_address[0]}\nCookies: {self.headers["Cookies"]}')
				except:
						print(f'GET {self.path} :\nFrom: {self.client_address[0]}\nCookies: ')
				
				if	args.file:
					f = open(args.file, 'r')
					content = f.read()
					f.close()
									
				else:
					content = "Move on mate."
					
				self.wfile.write(bytes(content, "utf-8"))
				
		except:
			pass




	def do_POST(self):

		try:
			if self.path == f'/{self.valid_endpoints["POST"]}':		
				self.server_version = "Apache/2.4.1"
				self.sys_version = ""
				self.send_response(200)
				self.send_header('Access-Control-Allow-Origin', '*')
				self.send_header('Content-Type', 'text/plain')
				self.end_headers()
				self.wfile.write(b'OK')
				real_action = self.headers["Action"]
				content_len = int(self.headers.get('Content-Length'))
				form_attrs = {'Action':self.headers.get("X-form-action"), 'Method':self.headers.get("X-form-method"), 'Enctype':self.headers.get("X-form-enctype"), 'Encoding':self.headers.get("X-form-encoding")}
				post_data = self.rfile.read(content_len)

		except:
			pass



	def do_OPTIONS(self):

		self.server_version = "Apache/2.4.1"
		self.sys_version = ""
		self.send_response(200)
		self.send_header('Access-Control-Allow-Origin', self.headers["Origin"])
		self.send_header('Vary', "Origin")
		self.send_header('Access-Control-Allow-Credentials', 'true')
		#self.send_header('Access-Control-Allow-Headers', 'X-form-responseHeaders')
		self.end_headers()
		self.wfile.write(b'OK')



	def log_message(self, format, *args):
		return



def main():

	try:
		server_port = args.port if args.port else 443

		try:
			httpd = HTTPServer(('0.0.0.0', server_port), Https_Server)

		except OSError:
			exit(f'\n[{FAILED}] Port {server_port} seems to already be in use.{END}\n')
		
		protocol = 'http'
		
		if args.cert and args.key:
			
			try:
				httpd.socket = ssl.wrap_socket (
					httpd.socket,
					keyfile = args.key,
					certfile = args.cert,
					server_side = True,
					ssl_version=ssl.PROTOCOL_TLS
				)
				
				protocol = 'https'
				
			except Exception as e:
				debug(f'Failed to establish SSL: {e}')
				exit(1)
		
			
		server = Thread(target = httpd.serve_forever, args = ())
		server.daemon = True
		server.start()
		print(f'[{INFO}] {protocol} server is up and running!')

		try:
			server_public_ip = check_output("curl --connect-timeout 3.14 -s ifconfig.me", shell = True).decode(sys.stdout.encoding)	
			
		except:
			server_public_ip = '127.0.0.1'
			pass
		
		for key,val in Https_Server.valid_endpoints.items():
			print(f'{INFO} {key} endpoint: {protocol}://{server_public_ip}:{server_port}/{val}')

		while True:
			sleep(5)
			
	except KeyboardInterupt:
		exit(0)
	
	except Exception as e:
		debug(f'Something went wrong: {e}')
		exit(1)	



if __name__ == '__main__':
	main()
