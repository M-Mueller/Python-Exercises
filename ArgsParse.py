import re

"""
>>> p = ArgParse()
>>> p.addOption('-p')
>>> '-p' in p.options
True
>>> args = ['-l 12']
>>> p.options['-p'](args)
True
>>> args
['-l 12']
"""
class ArgParse:
	def __init__(self):
		self.options = {}

	"""Adds an option that can either be set or not.
	"""
	def addOption(self, name):
		def parseValue(args):
			return True
		self.options[name] = parseValue

	def addInteger(self, name):
		def parseValue(args):
			if len(args) > 0:
				return int(args.pop(0))
			else:
				raise ValueError('Missing value for argument')
		self.options[name] = parseValue

	def addString(self, name):
		def parseValue(args):
			if(len(args) > 0):
				return args.pop(0)
			else:
				raise ValueError('Missing value for argument')
		self.options[name] = parseValue

	def parse(self, args):
		# a flag is a - together with a letter
		# flags must be either proceeded or succeeded by a space (except start/end of string)
		tokens = re.split('((?:^| )-[a-zA-Z](?= |$))', args)
		# remove all empty tokens and strip leading/trailing whitespace
		tokens = [t.strip() for t in tokens if t]

		result = {}
		while len(tokens) > 0:
			flag = tokens.pop(0)
			if not flag.startswith('-'):
				raise ValueError('Unexpected Value: ' + flag)
			if flag in self.options:
				result[flag] = self.options[flag](tokens)
			else:
				raise ValueError('Unkown Parameter: ' + flag)
		return result

if __name__ == '__main__':
	import doctest
	doctest.testmod()

	p = ArgParse()
	p.addOption('-l')
	p.addInteger('-p')
	p.addString('-d')
	print(p.parse('-l -p 8080 -d /usr-foo/logs'))
