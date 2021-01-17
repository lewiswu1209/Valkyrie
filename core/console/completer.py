import os
import sys
import re
import readline

COMMANDS = ["use", "back", "exit", "show", "quit", "set"]
COMMANDS_WITH_ARGS = ["use", "set", "show"]
SHOW_ARGS = ["options", "payloads"]
RE_SPACE = re.compile(".+\s+$", re.M)

class _Completer(object):

	cur_module = None
	
	def set_module(self, module):
		self.cur_module = module

	def _listdir(self, root):
		res = []
		for name in os.listdir(root):
			path = os.path.join(root, name)
			if os.path.isdir(path):
				name += os.sep
			res.append(name)
		return res

	def complete_show(self, args):
		return [p for p in SHOW_ARGS if p.startswith(args[0])]

	def complete_set(self, args):
		res = []
		results = []
		if self.cur_module is not None:
			res = self.cur_module.options.keys()
			results.extend([p for p in res if p.startswith(args[0])])
		if self.cur_module.payload is not None:
			res = self.cur_module.payload.options.keys()
			results.extend([p for p in res if p.startswith(args[0])])
			
		return results

	def complete_use(self, args):
		path = "%s/modules/%s" % (sys.path[0], args[-1])
		dirname, rest = os.path.split(path)
		res = []
		for p in self._listdir(dirname):
			if p.startswith(rest) and p != "__init__.py" and not p.endswith(".pyc"):
				if p.endswith(".py"):
					p = p[:-3]
				p = os.path.join(dirname, p)[len("%s/modules/" % (sys.path[0])):]
				res.append(p)
		return res

	def complete(self, text, state):
		buffer = readline.get_line_buffer()
		line = readline.get_line_buffer().split()

		if not line:
			return [c for c in COMMANDS][state]

		if RE_SPACE.match(buffer):
			line.append("")

		cmd = line[0].strip()
		if cmd in COMMANDS_WITH_ARGS:
			impl = getattr(self, "complete_%s" % cmd)
			args = line[1:]
			if args:
				return (impl(args) + [None])[state]
			return [cmd + " "][state]
		results = []
		for c in COMMANDS:
			if c.startswith(cmd):
				if c in COMMANDS_WITH_ARGS:
					results.append(c + " ")
				else:
					results.append(c)
		return results[state]

Completer = _Completer()
