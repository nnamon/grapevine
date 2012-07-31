import vboxapi
import PsYchic_VBInfo as VBInformation
from twisted.web import server, resource
from twisted.internet import reactor

class WebInterface(resource.Resource):
    isLeaf = True
    try:
		self.virtualBoxManager = vboxapi.VirtualBoxManager(None, None)
		self.virtualBox = self.virtualBoxManager.vbox
	except Exception, e:
		sys.exit("Please run the following command before re-running this program :\n\nexport PYTHONPATH=$PYTHONPATH:/usr/lib/virtualbox/:/usr/lib/virtualbox/sdk/bindings/xpcom/python/")

	def jsonResponse():
    	

    def render_GET(self, request):
        request.setHeader("content-type", "text/plain")
        return 'Request : ' + str(request)

reactor.listenTCP(8080, server.Site(WebInterface()))
reactor.run()