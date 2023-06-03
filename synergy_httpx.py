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
from string import ascii_uppercase, ascii_lowercase, digits
from platform import system as get_system_type
from copy import deepcopy

if get_system_type() == 'Linux':
	import gnureadline as global_readline
else:
	import readline as global_readline

filterwarnings("ignore", category = DeprecationWarning)

''' Colors '''
MAIN = '\001\033[38;5;85m\002'
GREEN = '\001\033[38;5;82m\002'
GRAY = PLOAD = '\001\033[38;5;246m\002'
NAME = '\001\033[38;5;228m\002'
RED = '\001\033[1;31m\002'
FAIL = '\001\033[1;91m\002'
ORANGE = '\001\033[0;38;5;214m\002'
LRED = '\001\033[0;38;5;196m\002'
BOLD = '\001\033[1m\002'
PURPLE = '\001\033[0;38;5;141m\002'
BLUE = '\001\033[0;38;5;12m\002'
UNDERLINE = '\001\033[4m\002'
UNSTABLE = '\001\033[5m\002'
END = '\001\033[0m\002'


''' MSG Prefixes '''
INFO = f'[{MAIN}Info{END}]'
WARN = f'[{ORANGE}Warning{END}]'
DBG = f'[{ORANGE}Debug{END}]'
IMPORTANT = f'[{ORANGE}Important{END}]'
FAILED = f'[{LRED}Error{END}]'
POST_REQ = f'[{PURPLE}POST-request{END}]'
GET_REQ = f'[{BLUE}GET-request{END}]'
META = '[\001\033[38;5;93m\002M\001\033[38;5;129m\002e\001\033[38;5;165m\002t\001\033[38;5;201m\002a\001\033[0m\002]'


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cert", action="store", help = "Your certificate.")
parser.add_argument("-k", "--key", action="store", help = "The private key for your certificate. ")
parser.add_argument("-p", "--port", action="store", help = "Server port.", type = int)
parser.add_argument("-q", "--quiet", action="store_true", help = "Do not print the banner on startup.")

args = parser.parse_args()


# -------------- General Functions -------------- #
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

	S = [['░', '█','▀','▀', '░'], ['░', '▀','▀','▄', '░'], ['░', '▀','▀','▀', '░']]
	Y = [['█', '░','░','█','░'], ['█', '▄','▄','█','░'], ['▄','▄','▄','▀','░']]
	N = [['█', '▀','▀','▄', '░'], ['█', '░','░','█','░'], ['▀', '░','░','▀','░']]
	E = [['█','▀','▀','▀', '░'], ['█','▀','▀','▀', '░'], ['▀','▀','▀', '▀', '░']]	
	R = [['█', '▀','▀','▄', '░'], ['█', '▄','▄','▀','░'], ['▀', '░', '▀','▀','░']]
	G = [['█','▀','▀','▀', '░'], ['█', '░','▀','▄' '░'], ['▀','▀','▀','▀','░']]
	Y = [['█', '░','░','█','░'], ['█', '▄','▄','█','░'], ['▄','▄','▄','▀','░']]
	H = [['░','░','█','░','░','█','░'], ['░','░','█', '█','▀','█','░'], ['░','░','█','░','░','█','░']]
	T = [['▀', '█','▀','░'], ['░', '█','░','░'], ['░', '█','░','░']]
	P = [['▄', '▀','▀','▄','░'], ['█', '▄','▄','█','░'], ['█','░','░','░','░']]
	X = [['█','░','░','█'], [' ', '▀','▄',''], ['█','░','░','█']]

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

		if charset < 2: final.append('\n  ')
	
	
	print(f"  {''.join(final)}")
	haxor_print('by t3l3machus', 48)


def print_meta():
	print(f'{META} Created by t3l3machus')
	print(f'{META} Follow on Twitter, HTB, GitHub: @t3l3machus')
	print(f'{META} Thank you!\n')


def print_green(msg):
	print(f'{GREEN}{msg}{END}')


def debug(msg):
	print(f'{DBG} {msg}{END}')


def failure(msg):
	print(f'{FAIL} {msg}{END}')


def restore_prompt():
	Main_prompt.rst_prompt() if Main_prompt.ready else Main_prompt.set_main_prompt_ready()


def print_to_prompt(msg):
	print('\r' + msg)
	restore_prompt()


def clone_dict_keys(_dict):	
	clone = deepcopy(_dict)
	clone_keys = clone.keys()
	return clone_keys


def print_columns(strings):
	
	columns, lines_ = os.get_terminal_size()
	mid = (len(strings) + 1) // 2
	max_length1 = max(len(s) for s in strings[:mid])
	max_length2 = max(len(s) for s in strings[mid:])

	if max_length1 + max_length2 + 4 <= columns:
		# Print the strings in two evenly spaced columns
		for i in range(mid):
			
			col1 = strings[i].ljust(max_length1)
			try: col2 = strings[i+mid].ljust(max_length2)
			except:	col2 = ''
			print(col1 + " " * 4 + col2)

	else:
		# Print the strings in one column
		max_length = max(len(s) for s in strings)

		for s in strings:
			print(s.ljust(max_length))

	print('\n', end='')


def get_file_contents(path):

	try:
		f = open(path, 'r')
		content = f.read()
		f.close()
		return [True, content]
	
	except Exception as e:
		return [False, e]


def chill():
	pass


# -------------- HTTPS Server -------------- #
class Synergy_Httpx(BaseHTTPRequestHandler):

	basic_endpoints = {
		'GET' : 'x3Rty7',
		'POST' : 'aWq8tY'
	}


	user_defined_endpoints = {
		'GET' : {
			# Below is an example endpoint, in case you wish to predifine a few
			'example-path-to-index' : '/var/www/html/index.html'
		},
	
		'POST' : {}
	}

	@staticmethod
	def get_endpoints():
		endpoints = list(Synergy_Httpx.user_defined_endpoints['GET'].keys())\
		+ list(Synergy_Httpx.user_defined_endpoints['POST'].keys())
		return endpoints.extend([Synergy_Httpx.basic_endpoints['GET'], Synergy_Httpx.basic_endpoints['POST']])


	@staticmethod
	def get_endpoint_local_path(endpoint, method):
		if endpoint in Synergy_Httpx.user_defined_endpoints[method].keys():
			return Synergy_Httpx.user_defined_endpoints[method][endpoint]
		return None


	def do_GET(self):
		
		try:
				
			response_body = Synergy_Httpx.get_endpoint_local_path(self.path[1:], 'GET')
			
			if self.path == f'/{self.basic_endpoints["GET"]}' or response_body:
				self.server_version = "Apache/2.4.1"
				self.sys_version = ""
				self.send_response(200)
				self.send_header('Content-type', 'text/javascript; charset=UTF-8')
				self.send_header('Access-Control-Allow-Origin', '*')
				self.end_headers()
				
				print_to_prompt(f'{GET_REQ} Received for {ORANGE}{self.path}{END} from {ORANGE}{self.client_address[0]}{END}')
				
				if	response_body:
					content = get_file_contents(response_body)

					if not content[0]:
						print_to_prompt(f'{FAILED} An error occured while reading the file associated with server path {ORANGE}{self.path}{END} ({content[1]})')
						content = [0, ""]

				else:
					content = [None, "Move on mate."]
					
				self.wfile.write(bytes(content[1], "utf-8"))
		except:
			pass
				


	def do_POST(self):

		try:
			response_body = Synergy_Httpx.get_endpoint_local_path(self.path[1:], 'POST')

			if self.path == f'/{self.basic_endpoints["POST"]}' or response_body:		
				self.server_version = "Apache/2.4.1"
				self.sys_version = ""
				self.send_response(200)
				self.send_header('Access-Control-Allow-Origin', '*')
				self.send_header('Content-Type', 'text/plain')
				self.end_headers()

				content_len = int(self.headers.get('Content-Length'))
				post_data = self.rfile.read(content_len)
				print_to_prompt(f'{POST_REQ} Received for {ORANGE}{self.path}{END} from {ORANGE}{self.client_address[0]}{END}')
				print_to_prompt(post_data.decode('utf-8', 'ignore').replace('<br>', '\n'))
				self.wfile.write(b'OK')

				if	response_body:
					content = get_file_contents(response_body)

					if not content[0]:
						print_to_prompt(f'{FAILED} An error occured while reading the file associated with server path {ORANGE}{self.path}{END} ({content[1]})')
						content = [None, ""]

			else:
				content = [None, "Move on mate."]
				
			self.wfile.write(bytes(content[1], "utf-8"))		

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



class PrompHelp:
	
	commands = {
				
		'serve' : {
			'details' : f'''
			\rCreates a mapping between an server path name and a local file to serve.
			\r
			\r {ORANGE}serve <GET|POST> <HTTP PATH NAME> <LOCAL FILE PATH>{END}
			''',
			'least_args' : 3,
			'max_args' : 3
		},			


		'release' : {
			'details' : f'''
			\rRemove a resource mapping (stop serving it).
			\r
			\r {ORANGE}release <HTTP PATH NAME>{END}
			''',
			'least_args' : 1,
			'max_args' : 1
		},	

		
		'help' : {
			'details' : f'''
			\rReally?
			''',
			'least_args' : 0,
			'max_args' : 1
		},

		'endpoints' : {
			'details' : f'''
			\rLists all available server endpoints.
			''',
			'least_args' : 0,
			'max_args' : 0
		},

		'exit' : {
			'details' : f'''
			\rTerminate the synergy server.
			''',
			'least_args' : 0,
			'max_args' : 0
		},

		'clear' : {
			'details' : f'''
			\rCome on man.
			''',
			'least_args' : 0,
			'max_args' : 0
		},
	
	}
	
	
	@staticmethod
	def print_main_help_msg():
				
		print(
		f'''
		\r  Command              Description
		\r  -------              -----------
		\r  help         [+]     Print this message.
		\r  serve        [+]     Add a resource to the synergy server's content.
		\r  release      [+]     Remove a resource from the synergy server's content.
		\r  endpoints            List all hosted resources.
		\r  clear                Clear screen.
		\r  exit                 Terminate the synergy server.
		\r  
		\r  Commands with [+] may require additional arguments.
		\r  For details use: {ORANGE}help <COMMAND>{END}
		''')
			


	@staticmethod
	def print_detailed(cmd):			
		print(PrompHelp.commands[cmd]['details']) if cmd in PrompHelp.commands.keys() else print(f'No details for command "{cmd}".')



	@staticmethod
	def validate(cmd, num_of_args):
		
		valid = True
		
		if cmd not in PrompHelp.commands.keys():
			print('Unknown command.')
			valid = False
			
		elif num_of_args < PrompHelp.commands[cmd]['least_args']:
			print('Missing arguments.')
			valid = False
		
		elif num_of_args > PrompHelp.commands[cmd]['max_args']:
			print('Too many arguments. Use "help <COMMAND>" for details.')
			valid = False			
	
		return valid


	
# Tab Auto-Completer		  
class Completer(object):
	
	def __init__(self):
		
		self.tab_counter = 0		
		self.main_prompt_commands = clone_dict_keys(PrompHelp.commands)
		self.generate_arguments = []
	
	
	def reset_counter(self):	
		sleep(0.4)
		self.tab_counter = 0
		
	
	def get_possible_cmds(self, cmd_frag):
		
		matches = []
		
		for cmd in self.main_prompt_commands:
			if re.match(f"^{cmd_frag}", cmd):
				matches.append(cmd)
		
		return matches
		
		
	def get_match_from_list(self, cmd_frag, wordlist):
		
		matches = []
		
		for w in wordlist:
			if re.match(f"^{cmd_frag}", w):
				matches.append(w)
		
		if len(matches) == 1:
			return matches[0]
		
		elif len(matches) > 1:
			
			char_count = 0
			
			while True:
				char_count += 1
				new_search_term_len = (len(cmd_frag) + char_count)
				new_word_frag = matches[0][0:new_search_term_len]
				unique = []
				
				for m in matches:
					
					if re.match(f"^{new_word_frag}", m):
						unique.append(m)		
				
				if len(unique) < len(matches):
					
					if self.tab_counter <= 1:
						return new_word_frag[0:-1]
						
					else:						
						print('\n')
						print_columns(matches)
						Main_prompt.rst_prompt()
						return False 
				
				elif len(unique) == 1:
					return False
				
				else:
					continue
					
		else:
			return False


	def find_common_prefix(self, strings):
		
		if not strings:
			return ""

		prefix = ""
		shortest_string = min(strings, key=len)

		for i, c in enumerate(shortest_string):

			if all(s[i] == c for s in strings):
				prefix += c
			else:
				break
		
		return prefix


	def path_autocompleter(self, root, search_term):
			
			# Check if root or subdir
			path_level = search_term.split(os.sep)
			
			if re.search(os.sep, search_term) and len(path_level) > 1:
				search_term	= path_level[-1]
				
				for i in range(0, len(path_level)-1):
					root += f'{os.sep}{path_level[i]}'
				
			dirs = next(os.walk(root))[1]
			match = [d + os.sep for d in dirs if re.match(f'^{re.escape(search_term)}', d)]

			files = next(os.walk(root))[2]
			match += [f for f in files if re.match(f'^{re.escape(search_term)}', f)]				

			# Appending match substring 
			typed = len(search_term)
			
			if len(match) == 1:				
				global_readline.insert_text(match[0][typed:])				
				self.tab_counter = 0
			else:				
				common_prefix = self.find_common_prefix(match)
				global_readline.insert_text(common_prefix[typed:])
				
			# Print all matches
			if len(match) > 1 and self.tab_counter > 1:
				print('\n')	
				print_columns(match)
				self.tab_counter = 0
				Main_prompt.rst_prompt()

				
	def update_prompt(self, typed, new_content, lower = False):
		global_readline.insert_text(new_content[typed:])		


	def complete(self, text, state):
		
		text_cursor_position = global_readline.get_endidx()
		self.tab_counter += 1
		line_buffer_val_full = global_readline.get_line_buffer().strip()
		line_buffer_val = line_buffer_val_full[0:text_cursor_position]
		#line_buffer_remains = line_buffer_val_full[text_cursor_position:]
		line_buffer_list = re.sub(' +', ' ', line_buffer_val).split(' ')
		line_buffer_list_len = len(line_buffer_list) if line_buffer_list != [''] else 0
		
		# Return no input or input already matches a command
		if (line_buffer_list_len == 0):
			return
			
		main_cmd = line_buffer_list[0].lower()
		
		# Get prompt command from word fragment
		if line_buffer_list_len == 1:
					
			match = self.get_match_from_list(main_cmd, self.main_prompt_commands)
			self.update_prompt(len(line_buffer_list[0]), match) if match else chill()
		
		
		# Autocomplete endpoints
		elif (main_cmd in ['release']) and (line_buffer_list_len > 1) and (line_buffer_list[-1][0] not in ["/", "~"]):
			
			if line_buffer_list[-1] in Synergy_Httpx.get_endpoints():
				pass
			
			else:			
				word_frag = line_buffer_list[-1]
				match = self.get_match_from_list(line_buffer_list[-1], Synergy_Httpx.get_endpoints())
				self.update_prompt(len(line_buffer_list[-1]), match) if match else chill()


		# Autocomplete help
		elif (main_cmd == 'help') and (line_buffer_list_len > 1):
									
			word_frag = line_buffer_list[-1].lower()
			match = self.get_match_from_list(line_buffer_list[-1], self.main_prompt_commands)
			self.update_prompt(len(line_buffer_list[-1]), match, lower = True) if match else chill()

		
		# Autocomplete paths	
		elif (main_cmd in ['serve']) and (line_buffer_list_len > 1) and (line_buffer_list[-1][0] in [os.sep, "~"]):
			
			root = os.sep if (line_buffer_list[-1][0] == os.sep) else os.path.expanduser('~')
			search_term = line_buffer_list[-1] if (line_buffer_list[-1][0] != '~') else line_buffer_list[-1].replace('~', os.sep)
			self.path_autocompleter(root, search_term)
			
		# Reset tab counter after 0.5s of inactivity
		Thread(name="reset_counter", target=self.reset_counter).start()
		return



''' Command Prompt Settings '''
class Main_prompt:
	
	original_prompt = prompt = f"{UNDERLINE}Synergy-httpx{END} > "
	ready = True
	SPACE = '#>SPACE$<#'
	exec_active = False

	
	@staticmethod
	def rst_prompt(prompt = prompt, prefix = '\r'):
		
		Main_prompt.ready = True
		Main_prompt.exec_active = False
		sys.stdout.write(prefix + Main_prompt.prompt + global_readline.get_line_buffer())


	@staticmethod
	def set_main_prompt_ready():
		Main_prompt.exec_active = False
		Main_prompt.ready = True


def main():

	print_banner() if not args.quiet else chill()

	try:
		server_port = args.port if args.port else 8080

		try:
			httpd = HTTPServer(('0.0.0.0', server_port), Synergy_Httpx)

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
		print(f'[{ORANGE}0.0.0.0{END}:{ORANGE}{server_port}{END}] Synergy {protocol} server is up and running!')

		try:
			server_public_ip = check_output("curl --connect-timeout 3.14 -s ifconfig.me", shell = True).decode(sys.stdout.encoding)	
			
		except:
			server_public_ip = '127.0.0.1'
			pass
		
		for key,val in Synergy_Httpx.basic_endpoints.items():
			print(f'{INFO} Basic {key} endpoint: {protocol}://{server_public_ip}:{server_port}/{val}')


	except KeyboardInterrupt:
		exit(0)
	
	except Exception as e:
		debug(f'Something went wrong: {e}')
		exit(1)	

	
	''' Start tab autoComplete '''
	comp = Completer()
	global_readline.set_completer_delims(' \t\n;')
	global_readline.parse_and_bind("tab: complete")
	global_readline.set_completer(comp.complete)			
		
	
	''' +---------[ Command prompt ]---------+ '''
	while True:
		
		try:
		
			if Main_prompt.ready:
								
				user_input = input(Main_prompt.prompt).strip()

				if user_input == '':
					continue

				# Handle single/double quoted arguments
				quoted_args_single = re.findall("'{1}[\s\S]*'{1}", user_input)
				quoted_args_double = re.findall('"{1}[\s\S]*"{1}', user_input)
				quoted_args = quoted_args_single + quoted_args_double
				
				if len(quoted_args):
					
					for arg in quoted_args:
						space_escaped = arg.replace(' ', Main_prompt.SPACE)
						
						if (space_escaped[0] == "'" and space_escaped[-1] == "'") or (space_escaped[0] == '"' and space_escaped[-1] == '"'):
							space_escaped = space_escaped[1:-1]
													
						user_input = user_input.replace(arg, space_escaped)
						
				
				# Create cmd-line args list
				user_input = user_input.split(' ')
				cmd_list = [w.replace(Main_prompt.SPACE, ' ') for w in user_input if w]
				cmd_list_len = len(cmd_list)
				cmd = cmd_list[0].lower() if cmd_list else ''
				
				# Validate number of args
				valid = PrompHelp.validate(cmd, (cmd_list_len - 1))				
									
				if not valid:
					continue


				if cmd == 'help':					
					if cmd_list_len == 1:
						PrompHelp.print_main_help_msg()
										
					elif cmd_list_len == 2:
						PrompHelp.print_detailed(cmd_list[1]) if cmd_list[1] in PrompHelp.commands.keys() \
						else print(f'Command {cmd_list[1] if len(cmd_list[1]) <= 10 else f"{cmd_list[1][0:4]}..{cmd_list[1][-4:]}" } does not exist.')
														

				elif cmd == 'serve':
					
					method = cmd_list[1].upper()
					# Check if user supplied a valid method
					if method not in ['GET', 'POST']:
						print('Illegal method.')
						continue

					# Check if path name already mapped
					if cmd_list[2] in Synergy_Httpx.get_endpoints():
						print('This endpoint is already mapped to a resource.')
						continue					   
					
					# Check if path to local file is valid
					if not os.path.isfile(cmd_list[3]):
						print('File not found.')
						continue	
					
					Synergy_Httpx.user_defined_endpoints[method][cmd_list[2]] = cmd_list[3]
					print(f'Resource mapping succesfully added!')


				elif cmd == 'release':
		
					# Check if path name is mapped
					if cmd_list[1] not in Synergy_Httpx.user_defined_endpoints[method].keys():
						print('Endpoint not found.')
						continue					   
					
					del Synergy_Httpx.user_defined_endpoints[method][cmd_list[1]]
					print(f'Resource mapping succesfully removed.')				
					continue


				elif cmd == 'endpoints':
					print(f'\n{BOLD}Basic endpoints{END}:')
					for method in Synergy_Httpx.basic_endpoints.keys():
						print(f'/{Synergy_Httpx.basic_endpoints[method]} ({method})')

					print(f'\n{BOLD}User Defined{END}:')
					for method in Synergy_Httpx.user_defined_endpoints.keys():
						for key,value in Synergy_Httpx.user_defined_endpoints[method].items():
							print(f'/{key} : {value} ({method})')
					print('')


				elif cmd == 'clear':
					os.system('clear')


				elif cmd == 'exit':
					raise KeyboardInterrupt

				else:
					continue

		except KeyboardInterrupt:
			
			Main_prompt.ready = True			
			choice = input('\nAre you sure you wish to exit? [y/n]: ').lower().strip()
			verified = True if choice in ['yes', 'y'] else False
										
			if verified:								
				print_meta()
				sys.exit(0)			


if __name__ == '__main__':
	main()
