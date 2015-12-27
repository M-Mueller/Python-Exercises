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
		# split at space and remove empty elements
		args = [s for s in args.split(' ') if s]
		result = {}
		while len(args) > 0:
			flag = args.pop(0)
			if not flag.startswith('-'):
				raise ValueError('Unexpected Value: ' + flag)
			if flag in self.options:
				result[flag] = self.options[flag](args)
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
	print(p.parse('-l -p 8080 -d /usr/logs '))
