import readline

from core.console.completer import Completer

from importlib import import_module

prompt = "Valkyrie > "

cur_module = None

def get_cmd():
	readline.set_completer_delims(' \t\n;')
	readline.parse_and_bind("tab: complete")
	readline.set_completer(Completer.complete)

	command = raw_input(prompt).lower()

	return command

def do_use(cmd_line):
	global prompt
	global cur_module

	try:
		cur_module = import_module( "modules.%s" % (cmd_line.replace('/','.')) )
		Completer.set_module(cur_module)
		prompt = "Valkyrie (%s) > " % (cmd_line)
	except ImportError:
		print("Can not find this module.")
		cur_module = None
		Completer.set_module(cur_module)
		prompt = "Valkyrie > "
	except KeyError:
		print("Please specify a module.")
		cur_module = None
		Completer.set_module(cur_module)
		prompt = "Valkyrie > "

def do_back():
	global prompt
	global cur_module
	
	cur_module = None
	Completer.set_module(cur_module)
	prompt = "Valkyrie > "

def do_show_options():
	if cur_module is not None:
		print("Name\t\tCurrent Setting\t\tRequired\tDescription")
		print("----\t\t---------------\t\t--------\t-----------")
		for key,value in cur_module.options.items():
			name = (key + "\t\t") if len(key) < 8 else (key + "\t")
			cur_setting = value["current_setting"] + "\t\t\t"
			required = "yes" if value["required"] else "no"
			description = value["description"]
			print("%s%s%s\t\t%s" % (name, cur_setting, required, description))
	else:
		print("Please use 'use' command to select one module first")

def do_show(cmd_line):
	if cmd_line == "options":
		do_show_options()
	elif cmd_line == "payloads":
		do_show_payloads()
	else:
		print("[-] Argument required")
		print("")
		print("[*] Valid parameters for the \"show\" command are: info, options")

def do_set(cmd_line):
	options = cmd_line.split()
	if cur_module is not None:
		for key,value in cur_module.options.items():
			if key == options[0].upper():
				value["current_setting"] = options[1]
	else:
		print("Please use 'use' command to select one module first")

def lst_cmd():
	print("lst")

def help():
	cur_module.help()

def do_cmd():
	cmd_line = get_cmd().strip()

	if cmd_line.startswith("use "):
		do_use(cmd_line[4:])
	elif cmd_line == "use":
		print("Please specify a module.")
	elif cmd_line == "back":
		do_back()
	elif cmd_line.startswith("show "):
		do_show(cmd_line[5:])
	elif cmd_line == "show":
		print("[-] Argument required")
		print("")
		print("[*] Valid parameters for the \"show\" command are: info, options")
	elif cmd_line.strip() == "options":
		do_options()
	elif cmd_line == "list" or cmd_line == "lst":
		lst_cmd()
	elif cmd_line.startswith("set "):
		do_set(cmd_line[4:])
	elif cmd_line.strip() == "help":
		help()
	elif cmd_line.strip() == "exit" or cmd_line.strip() == "quit" or cmd_line.strip() == "bye":
		exit()
	elif cmd_line.strip() == "":
		pass
	else:
		print("Unknown Command : %s" % cmd_line)

