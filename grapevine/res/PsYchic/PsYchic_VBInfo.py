import vboxapi
import sys
import os

class Information(object):

	def __init__(self):
		try:
			self.virtualBoxManager = vboxapi.VirtualBoxManager(None, None)
			self.virtualBox = self.virtualBoxManager.vbox	
		except Exception, e:	#  This error occurs when the PYTHONPATH is not set to virtualbox directory			
			sys.exit("Please run the following command before re-running this program :\n\nexport PYTHONPATH=$PYTHONPATH:/usr/lib/virtualbox/:/usr/lib/virtualbox/sdk/bindings/xpcom/python/")

	def listAllMachines(self):
		print "List of availabe VirtualBox machines :\n"
		virtualBoxConstants = self.virtualBoxManager.constants
		for machine in self.virtualBoxManager.getArray(self.virtualBox, 'machines'):
			print "[%s]" %(machine.name)
			print "'--State: 		%s" %(self.enumToString(virtualBoxConstants, "MachineState", machine.state))
			print "'--Session state:	%s" %(self.enumToString(virtualBoxConstants, "SessionState", machine.sessionState))
			print "'--ID: 			%s\n" %machine.id

	def checkIfAlive(IPAddress):
		commandString = "ping -c 1 " + IPAddress
		resultVariable = os.system(commandString)

		if resultVariable == 0:
			return True
		else:
			return false

	#
	# Converts an enumeration to a printable string.
	#
	def enumToString(self, constants, enumerate, element):
		all = constants.all_values(enumerate)
		for key in all.keys():
			if str(element) == str(all[key]):
				return key

