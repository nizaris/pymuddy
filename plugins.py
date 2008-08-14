from EnabledPlugins.antitheft import AntiTheft
import re

class Trigger:
	def __init__( self, parser, name, regexp, funcObj, enabled):
		self.regexp	= regexp
		self.funcObj	= funcObj
		self.regex	= re.compile( regexp)
		self.enabled	= enabled
		self.parser	= parser
	
	def check( self, data):
		print "Trigger.check()"
		if self.enabled:
			matchObj = self.regex.match( data)
			if matchObj:
				print "Trigger matched"
				self.funcObj( matchObj)
				raise NameError
		
	def enable( self):
		self.enabled = True
	
	def disable( self):
		self.enabled = False

class Alias:
	def __init__( self, parser, name, regexp, funcObj, enabled):
		self.regexp	= regexp
		self.funcObj	= funcObj
		self.regex	= re.compile( regexp)
		self.enabled	= enabled
		self.parser	= parser
	
	def check( self, data):
		if self.enabled:
			matchObj = self.regex.match( data)
			if matchObj:
				self.funcObj( matchObj)
				raise NameError
	
	def enable( self):
		self.enabled = True
	
	def disable( self):
		self.enabled = False

class Parser:
	def __init__( self, factory):
		self.factory	= factory
		self.triggers	= {}
		self.aliases	= {}
		self.antitheft	= AntiTheft( self)
	
	def parseTriggers( self, line):
		print "Parser.parseTriggers()"
		doWrite = True
		for trigger in self.triggers.values():
			try:
				trigger.check( line)
			except NameError:
				doWrite = False
				break
		if doWrite:
			self.factory.write( line)
	
	def parseAliases( self, data):
		doSend = True
		for name, alias in self.aliases.items():
			try:
				alias.check( data, self.factory)
			except NameError:
				doSend = False
				break
		if doSend:
			self.factory.send( data)

	def enableTrigger( nameRegexp):
		regex = re.compile( nameRegexp)
		for name, trigger in self.triggers:
			if regex.match( name):
				trigger.enable()

	def disableTrigger( nameRegexp):
		regex = re.compile( nameRegexp)
		for name, trigger in self.triggers:
			if regex.match( name):
				trigger.disable()

	def enableAlias( nameRegexp):
		regex = re.compile( nameRegexp)
		for name, alias in self.aliases:
			if regex.match( name):
				alias.enable()

	def disableAlias( nameRegexp):
		regex = re.compile( nameRegexp)
		for name, alias in self.aliases:
			if regex.match( name):
				alias.disable()
	
	def addAlias( self, name, regexp, funcObj, enabled=True):
		self.aliases[name] = Alias( self, name, regexp, funcObj, enabled)
	
	def addTrigger( self, name, regexp, funcObj, enabled=True):
		self.triggers[name] = Trigger( self, name, regexp, funcObj, enabled)
	
	def delAlias( self, nameRegexp):
		regex = re.compile( nameRegexp)
		for name, alias in self.aliases:
			if regex.match( name):
				del self.aliases[name]
	
	def delTrigger( self, nameRegexp):
		regex = re.compile( nameRegexp)
		for name, trigger in self.triggers:
			if regex.match( name):
				del self.triggers[name]
	
	def write( self, data):
		self.factory.write( data)
	
	def send( self, data):
		self.factory.send( data)

