import yaml
import hashlib

def loadNotes(lang, filename):
	result = None
	try:
		f = open("assets/notes/" + lang + "/" + filename, "r")
		result = f.read()
		f.close()
	except:
		print "WARNING: Unable to load notes for " + lang + "/" + filename
	if (result == None and lang != "en"):
		return loadNotes("en", filename)
	elif (result != None):
		return result
	else:
		return None

def inflateItems(items, lang):
	for key, category in items.iteritems():
		for item in category:
			if (item.get("notes") != None):
				item["notes"] = loadNotes(lang, item["notes"])
				if (item["notes"] == None): item.pop("notes", None)
			if (item.get("app") != None):
				item["identifier"] = hashlib.sha256(str(item["app"])).hexdigest()
	return items

def inflateConfig(config, params):
	config["firmwares"] = inflateItems(config["firmwares"], params.get("lang", "en")[0])
	config["applications"] = inflateItems(config["applications"], params.get("lang", "en")[0])
	return config

lastConfig = None
def getConfig(provider, params):
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
		lastConfig = inflateConfig(config, params)
		return config
	else:
		raise Exception("Unable to load config file")

 
class LedgerUpdateAPI:
	def getLastFirmware(self, handler, path, params):
		return (500, {"not": "implemented"})

	def getFirmwares(self, handler, path, params):
		try:
			return (200, getConfig(params.get("provider", [""])[0], params)["firmwares"])
		except:
			return (404, {"error": "Provider not found"})

	def getApplications(self, handler, path, params):
		try:
			return (200, getConfig(params.get("provider", [""])[0], params)["applications"])
		except:
			return (404, {"error": "Provider not found"})

	def notFound(self, handler, path, params):
		return (404, {"error": "Call not found"})
