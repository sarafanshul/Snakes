import os ,subprocess
DEBUG = False
os.system('color')
from colorama import Fore, Back, Style , init
 
# print(Style.DIM + 'and in dim text') 

def print_Info():
	with open ('static/fancy.txt' ,'r') as dsgn:
		for line in dsgn :
			print(Fore.WHITE + '  '*4 ,end = '')
			print(Fore.RED + line.rstrip())
			# print('  '*4 ,end = '')
			# print(line.rstrip())=
	print(Style.RESET_ALL)

def main():
	# initialization
	if not DEBUG:
		subprocess.run(['cls'] , shell = True)

	# logo onscr
	print_Info()
	import snake
	snake.main()

if __name__ == '__main__':
	main()