#!/bin/python3
#
# Author: Panagiotis Chartas (t3l3machus)
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
POST_DATA = f'[{PURPLE}Post-data{END}]'

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cert", action="store", help = "Your certificate.")
parser.add_argument("-k", "--key", action="store", help = "The private key for your certificate. ")
parser.add_argument("-p", "--port", action="store", help = "Server port.", type = int)
parser.add_argument("-f", "--file", action="store", help = "File to be served via GET.")

args = parser.parse_args()

def haxor_print(text, leading_spaces = 0):

	text_chars = list(text)
	current, mutated = '', ''

	for i in range(len(text)):
		
		original = text_chars[i]
		current += original
		mutated += f'\033[1;38;5;82m{text_chars[i].upper()}\033[0m'
		print(f'\r{" " * leading_spaces}{mutated}', end = '')
		sleep(0.05)
		print(f'\r{" " * leading_spaces}{current}', end = '')
		mutated = current

	print(f'\r{" " * leading_spaces}{text}\n')


def print_banner():

	padding = '  '

	S = [['░', '█','▀','▀', '░'], ['░', '▀','▀','▄', '░'], ['░', '▀','▀','▀', '░']]
	Y = [['█', '░','░','█','░'], ['█', '▄','▄','█','░'], ['▄','▄','▄','▀','░']]
	N = [['█', '▀','▀','▄', '░'], ['█', '░','░','█','░'], ['▀', '░','░','▀','░']]
	E = [['█','▀','▀','▀', '░'], ['█','▀','▀','▀', '░'], ['▀','▀','▀', '▀', '░']]	
	R = [['█', '▀','▀','▄', '░'], ['█', '▄','▄','▀','░'], ['▀', '░', '▀','▀','░']]
	G = [['█','▀','▀','▀', '░'], ['█', '░','▀','▄' '░'], ['▀','▀','▀','▀','░']]
	Y = [['█', '░','░','█','░'], ['█', '▄','▄','█','░'], ['▄','▄','▄','▀','░']]
	H = [['░','░','░','█','░','░','█','░'], ['░','░','░','█', '▀','▀','█','░'], ['░','░','░','▀','░','░','▀','░']]
	T = [['▀', '█','▀','░'], ['░', '█','░','░'], ['░', '█','░','░']]
	P = [['▄', '▀','▀','▄','░'], ['█', '▄','▄','█','░'], ['█','░','░','░','░']]
	X = [['█','░','█'], ['▄', '▀','▄'], ['▀','░','▀']]

	banner = [S,Y,N,E,R,G,Y,H,T,T,P,X]
	final = []
	print('\r')
	init_color = 31
	txt_color = init_color
	cl = 0

	for charset in range(0, 3):
		for pos in range(0, len(banner)):
			for i in range(0, len(banner[pos][charset])):
				clr = f'\033[38;5;{txt_color}m'
				char = f'{clr}{banner[pos][charset][i]}'
				final.append(char)
				cl += 1
				txt_color = txt_color + 36 if cl <= 3 else txt_color

			cl = 0

			txt_color = init_color
		init_color += 31

		if charset < 2: final.append('\n   ')
	
	
	print(f"   {''.join(final)}")
	haxor_print('by t3l3machus', 49)



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
				post_data = self.rfile.read(content_len)
				print(f'{POST_DATA} Received from {self.client_address[0]}')
				print(post_data.decode('utf-8', 'ignore').replace('<br>', '\n'))
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
	print_banner()
	try:
		server_port = args.port if args.port else 443

		try:
			httpd = HTTPServer(('0.0.0.0', server_port), Https_Server)

		except OSError:
			exit(f'\n{FAILED} Port {server_port} seems to already be in use.{END}\n')
		
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
		print(f'{INFO} Synergy {protocol} server is up and running!')

		try:
			server_public_ip = check_output("curl --connect-timeout 3.14 -s ifconfig.me", shell = True).decode(sys.stdout.encoding)	
			
		except:
			server_public_ip = '127.0.0.1'
			pass
		
		for key,val in Https_Server.valid_endpoints.items():
			print(f'{INFO} {key} endpoint: {protocol}://{server_public_ip}:{server_port}/{val}')

		while True:
			sleep(5)
			
	except KeyboardInterrupt:
		exit(0)
	
	except Exception as e:
		debug(f'Something went wrong: {e}')
		exit(1)	



if __name__ == '__main__':
	main()
