
import yaml

lastConfig = None
def getConfig(provider):
	config = None
	filename = "config"
	if (len(provider) != 0):
		filename += "_" + provider
	filename += ".yml"
	with open(filename, 'r') as stream:
		config = yaml.load(stream)
	if (config == None and lastConfig != None):
		print "WARNING: An error happened during config loading."
		return lastConfig;
	elif (config != None):
		lastConfig = config
		return config
	else:
		raise Exception("Unable to load config file")

 
class LedgerUpdateAPI:
	def getLastFirmware(self, handler, path, params):
		return (500, {"not": "implemented"})

	def getFirmwares(self, handler, path, params):
		try:
			return (200, getConfig(params.get("provider", [""])[0])["firmwares"])
		except:
			return (404, {"error": "Provider not found"})

	def getApplications(self, handler, path, params):
		try:
			return (200, getConfig(params.get("provider", [""])[0])["applications"])
		except:
			return (404, {"error": "Provider not found"})

	def notFound(self, handler, path, params):
		return (404, {"error": "Call not found"})
