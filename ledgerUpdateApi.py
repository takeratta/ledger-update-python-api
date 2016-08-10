
import yaml

config = None
with open("config.yml", 'r') as stream:
    config = yaml.load(stream)
 
class LedgerUpdateAPI:
	def getLastFirmware(self, handler):
		return (500, {"not": "implemented"})

	def getFirmwares(self, handler):
		return (200, config["firmwares"])

	def getApplications(self, handler):
		return (200, config["applications"])

	def notFound(self, handler):
		return (404, {"error": "Call not found"})
