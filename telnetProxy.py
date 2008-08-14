from twisted.internet.protocol import ClientFactory, Protocol, Factory
from twisted.internet import reactor as serverReactor
from twisted.conch.telnet import TelnetProtocol, TelnetTransport, GA
from twisted.protocols.basic import LineReceiver
from plugins import Parser
from sys import exit

# This file creates a telnet proxy, connecting to achaea.com.
# The file works like this:
#
# Local client --> TelnetServer() --> TelnetClient() --> Achaea

class TelnetClient( TelnetProtocol):
	"""
	TelnetClient() connects directly to the Achaea server.
	"""
	
	myServer = None
	factory = None
	buffer = ""

	def dataReceived( self, bytes):
		"""
		If you want to add triggers, they would go here.
		"""
		
		self.buffer += bytes
		lines = self.buffer.split( "\n")
		self.buffer = lines.pop()
		#lines.append( self.buffer)
		for line in lines:
			self.factory.parseTriggers( line)
	
	def connectionMade( self):
		self.transport.commandMap[GA] = self.handleGA
	
	def handleGA( self, other):
		"""
		Not sure yet.
		"""
		
		self.factory.parseTriggers( self.buffer)
		self.buffer = ""


class TelnetClientFactory( ClientFactory):
	"""
	TelnetClientFactory() is magic. Do not edit.
	"""

	myClient = TelnetTransport( TelnetClient)
	
	def startedConnected( self, connector):
		print "Started to connect."
	
	def buildProtocol( self, addr):
		print "Connected."
		return self.myClient
	
	def clientConnectionLost( self, connector, reason):
		print "Lost connection. Reason:", reason
		exit()
	
	def clientConnectionFailed( self, connector, reason):
		print "Connection failed. Reason:", reason

class TelnetServer( Protocol):
	"""
	Local client connects to TelnetServer().
	TelnetServer() connects to TelnetClient()
	"""
	
	myClient = None
	factory = None
	
	def connectionMade( self):
		"""
		Local client connected. Start client connection to server.
		"""
		
		self.transport.write( "Connected to PyMuddy\n")
		telnetClientFactory = TelnetClientFactory()
		self.myClient = telnetClientFactory.myClient
		self.myClient.myServer = self
		self.myClient.factory = self.factory
		
		# To use VadiSystem, change "achaea.com" to "localhost"
		# and 23 to 1234.
		serverReactor.connectTCP( "localhost", 1234, telnetClientFactory)
		serverReactor.run()
	
	def dataReceived( self, data):
		"""
		Input received; forward data to myClient's transport.
		
		Further, if you would like to add aliases, the code
		should go here.
		"""
		
		self.factory.parseAliases( data)
	
	def write( self, data):
		self.transport.write( "%s\n" % data)
	
	def send( self, data):
		self.myClient.transport.write( "%s\n" % data)
		self.transport.write( "\x1b[1;33%s\x1b[0m\n" % data)
	
	def connectionLost( self):
		exit()

class MyFactory( Factory):
	p = None
	parser = None
	
	def buildProtocol( self, addr):
		self.p = self.protocol()
		self.p.factory = self
		self.parser = Parser( self)
		return self.p
	
	def write( self, data):
		self.p.write( data)
	
	def send( self, data):
		self.p.send( data)
	
	def parseTriggers( self, data):
		self.parser.parseTriggers( data)
	
	def parseAliases( self, data):
		self.parser.parseAliases( data)