from ledgerblue.commException import CommException
import json
from threading import Thread, Lock
import binascii

class Params(dict):
    __getattr__= dict.__getitem__
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__

class ScriptRunner(Thread):

    def __init__(self, client, script, params):
        Thread.__init__(self)
        self.client = client
        self.script = script
        p = Params()
        p.url = "https://hsmprod.hardwarewallet.com/hsm/process"
        p.apdu = True
        p.rootPrivateKey = None
        p.deployLegacy = False
        try:
            for key, value in params.iteritems():
                print "set " + key + " " + value[0]
                setattr(p, key, value[0])
        except Exception, Reason:
            print str(Reason)
        print p
        self.params = p
        self.lock = Lock()
        self.lock.acquire()
        self.nonce = 0
        self.response = {}
        self.daemon = True

    def run(self): 
        script = self.script
        try:
            script(self, self.params)
            self.client.sendMessage(json.dumps({"query": "success"}) + u'')
            self.client.close()
        except Exception, Reason:
            self.handleError(str(Reason))

    def handleError(self, message):
        self.client.sendMessage(json.dumps({"query": "error", "data": message}) + u'')
        self.client.close()

    def exchange(self, apdu):
        """ Called from the script thread """
    	lock = self.lock
        self.nonce += 1
    	self.client.sendMessage(json.dumps({"query": "exchange", "data": binascii.hexlify(apdu), "nonce": self.nonce}) + u'')
        lock.acquire(True)
        lock.release()
        print self.response
        if (self.response["response"] == "error"):
            sw = int(self.response["data"], 16)
            raise CommException("Invalid status %04x" % sw, sw)
        elif (self.response["response"] != "success"):
            raise Exception("Fatal error")
        else:
            return bytearray.fromhex(self.response["data"])
        
    def bulkExchange(self, apdus):
        """ Called from the script thread """
        lock = self.lock
        self.nonce += 1
        data = []
        for apdu in apdus:
            data.append(binascii.hexlify(apdu))
        self.client.sendMessage(json.dumps({"query": "bulk", "data": data, "nonce": self.nonce}) + u'')
        lock.acquire(True)
        lock.release()
        print self.response
        if (self.response["response"] == "error"):
            sw = int(self.response["data"], 16)
            raise CommException("Invalid status %04x" % sw, sw)
        elif (self.response["response"] != "success"):
            raise Exception("Fatal error")

    def handleMessage(self, message): 
    	""" Called from the server thread """
    	if (self.lock == None):
    		""" Drop the message """
    		return
    	return
