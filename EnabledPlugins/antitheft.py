class AntiTheft:
	def __init__( self, parser):
		self.parser = parser
		parser.addTrigger( "at_unwornPack", "^You remove a canvas backpack\.$", self.rewearPack)
		
	def rewearPack( self, matchObj):
		self.parser.send( "wear pack")
		self.parser.write( matchObj.group( 0))