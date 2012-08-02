import json
import vboxapi
import vbinfo as VBInformation
from twisted.web import server, resource
from twisted.internet import reactor

class WebInterface(resource.Resource):
    isLeaf = True
    VBInfo = VBInformation.Information()

    def generateJSONResponse(self):
    	VirtualBoxObject = "{ 'Machines' : " + self.VBInfo.jsonifyMachinesData() + ", "
    	VirtualBoxObject += "'crashedMachines' : '" + self.VBInfo.getCrashedMachines() + "' }"
    	VirtualBoxObjectJSON = json.dumps(eval(VirtualBoxObject), sort_keys=True, indent=3)
    	return VirtualBoxObjectJSON

    def render_GET(self, request):
        request.setHeader("content-type", "text/plain")
        request.setHeader("Access-Control-Allow-Origin", "*")
        return self.generateJSONResponse()

reactor.listenTCP(8080, server.Site(WebInterface()))
reactor.run()