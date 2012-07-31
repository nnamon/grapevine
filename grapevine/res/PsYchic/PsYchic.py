import PsYchic_VBCtrl as VBControl
import PsYchic_VBInfo as VBInformation
import os
import sys
from optparse import OptionParser

def main():
	if len(sys.argv) == 1:
		print "Use --help for a list of options."

	description = "PsYchic is an interactive Virtual Box controller using both command line and a web interface."
	parser = OptionParser(description=description)
	parser.add_option("-l", "--list", action="store_true", dest="list", default=False, help="List all Virtual Boxes on this machine.")
	parser.add_option("-a", "--activate", type="string", dest="vb_name", default='',help="Activate a Virtual Box by name")
	parser.add_option("-g", "--activateGUI", type="string", dest="vb_name_gui", default='',help="Activate a Virtual Box by name with GUI")
	parser.add_option("-o", "--turnoff", type="string", dest="vb_turnoff", default='',help="Turn Off a Virtual Box by ID")
	parser.add_option("-w", "--webui", type="int", dest="port_number", default=8080, help="Use PsYchic from via a web interface.")
	(options, args) = parser.parse_args()

	if options.list:
		listAllMachines()
	elif options.vb_name:
		activateMachine(options.vb_name, False)
	elif options.vb_name_gui:
		activateMachine(options.vb_name_gui, True)
	elif options.vb_turnoff:
		shutdownMachine(options.vb_turnoff)


def listAllMachines():
	VBInfo = VBInformation.Information()
	VBInfo.listAllMachines()

def activateMachine(name, gui):
	VirtualBox = VBControl.Controller()
	print "Starting " + name
	VirtualBox.activateMachine(name, gui)

def shutdownMachine(vbID):
	VirtualBox = VBControl.Controller()
	print "Shutting Down " + vbID
	VirtualBox.dumpGuestCore(vbID)

#ldef commandMachine(vm, command, arguments):

if __name__ == '__main__':
	main()

