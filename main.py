from twisted.internet.protocol import Factory
from twisted.internet import reactor
import telnetProxy

factory = telnetProxy.MyFactory()
factory.protocol = telnetProxy.TelnetServer
reactor.listenTCP( 8007, factory)
reactor.run()