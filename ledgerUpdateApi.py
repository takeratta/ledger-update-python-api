
import yaml

lastConfig = None
def getConfig():
	config = None
	with open("config.yml", 'r') as stream:
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
	def getLastFirmware(self, handler):
		return (500, {"not": "implemented"})

	def getFirmwares(self, handler):
		return (200, getConfig()["firmwares"])

	def getApplications(self, handler):
		return (200, getConfig()["applications"])

	def notFound(self, handler):
		return (404, {"error": "Call not found"})
