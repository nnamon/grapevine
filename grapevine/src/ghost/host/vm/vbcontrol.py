import os
import sys
import vboxapi
import time

class Controller(object):

	def __init__(self):
		try:
			self.virtualBoxManager = vboxapi.VirtualBoxManager(None, None)
			self.virtualBox = self.virtualBoxManager.vbox	
		except Exception, e:	#  This error occurs when the PYTHONPATH is not set to virtualbox directory
			sys.exit("Please run the following command before re-running this program :\n\nexport PYTHONPATH=$PYTHONPATH:/usr/lib/virtualbox/:/usr/lib/virtualbox/sdk/bindings/xpcom/python/")

			
	def getMachineById(self, mid):
		try:
			machine = self.virtualBox.getMachine(mid)
		except:
			machine = self.virtualBox.findMachine(mid)

		return machine

	def activateMachine(self, mid, gui):
		virtualMachine = self.getMachineById(mid)
		self.session = self.virtualBoxManager.mgr.getSessionObject(self.virtualBox)
		if gui:
			progress = virtualMachine.launchVMProcess(self.session, "gui", "")
		else:
			progress = virtualMachine.launchVMProcess(self.session, "vrdp", "")
		progress.waitForCompletion(-1)
		self.session.unlockMachine()


	def commandMachine(self, vmID, command, arguments):
		machine = self.getMachineById(vmID)
		session = self.virtualBoxManager.mgr.getSessionObject(self.virtualBox)
		machine.lockMachine(session, self.virtualBoxManager.constants.LockType_Shared)
		if session.state != self.virtualBoxManager.constants.SessionState_Locked:
			session.unlockMachine()

		console = session.console
		options = {
			'shutdown':			lambda: console.powerDown(),
			'takeSnapshot':		lambda: console.takeSnapshot(),
			'deleteSnapshot':	lambda: console.deleteSnapshot(arguments),
			'restoreSnapshot':	lambda:	console.restoreSnapshot(arguments),
			'pause':			lambda: console.pause(),
			'resume':			lambda: console.resume(),
			'getDumpFiles':		lambda: console.debugger.dumpGuestCore(arguments, None)
		}

		try:
			executionProgress = options[command]()
			if executionProgress:
				while not executionProgress.completed:
					executionProgress.waitForCompletion(-1)
				if executionProgress.completed and int(executionProgress.resultCode) == 0:
					print 'Completed'
				else:
					session.unlockMachine()
					return False
		except Exception, e:
			print e

		session.unlockMachine()
		return True

	def shutdownMachine(self, vbID):
		self.commandMachine(vbID, 'shutdown', None)

	def dumpGuestCore(self, vbID):
		filename = str(int(time.time()))
		filename += ".dump"
		self.commandMachine(vbID, 'getDumpFiles', filename)




	
