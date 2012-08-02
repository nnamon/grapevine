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

	def jsonifyMachinesData(self):
		jsonString = "["
		virtualBoxConstants = self.virtualBoxManager.constants
		for machine in self.virtualBoxManager.getArray(self.virtualBox, 'machines'):
			jsonString += "{"
			jsonString += "'MachineState' : '" + str(self.enumToString(virtualBoxConstants, "MachineState", machine.state)) + "',"
			jsonString += "'SessionState' : '" + str(self.enumToString(virtualBoxConstants, "SessionState", machine.state)) + "',"
			jsonString += "'MachineID' : '" + str(machine.id) + "',"
			jsonString += "'MachineOS' : '" + str(machine.OSTypeId) + "',"
			jsonString += "'MachineMemSize' : '" + str(machine.memorySize) + "',"
			jsonString += "'MachineName' : '" + str(machine.name) + "'"
			jsonString += "},"

		jsonString += "]"
		return jsonString
	def getAllLiveMachinesID(self):
		livemachinesID = []
		virtualBoxConstants = self.virtualBoxManager.constants
		for machine in self.virtualBoxManager.getArray(self.virtualBox, 'machines'):
			machineState = self.enumToString(virtualBoxConstants, "MachineState", machine.state)
			if machineState == "Running":
				livemachinesID.append(machine.id)
		if livemachinesID == None:
			return [0]
		else:
			return livemachinesID
		
	def getCrashedMachines(self):
		## ToDo to return a list of vbID that hanged
		crashedMachinesID = []
		virtualBoxConstants = self.virtualBoxManager.constants
		for machine in self.virtualBoxManager.getArray(self.virtualBox, 'machines'):
			machineState = self.enumToString(virtualBoxConstants, "MachineState", machine.state)
			if machineState == "Aborted":
				crashedMachinesID.append(machine.id)
			elif machineState == "Paused":
				crashedMachinesID.append(machine.id)

		if crashedMachinesID != None:
			return crashedMachiensID
		else:
			return "0"		## For JavaScript to interpret

	def checkIfAlive(self, IPAddress):
		commandString = "ping -c 1 " + IPAddress
		resultVariable = os.system(commandString)

		if resultVariable == 0:
			return True
		else:
			return False

	#
	# Converts an enumeration to a printable string.
	#
	def enumToString(self, constants, enumerate, element):
		all = constants.all_values(enumerate)
		for key in all.keys():
			if str(element) == str(all[key]):
				return key

