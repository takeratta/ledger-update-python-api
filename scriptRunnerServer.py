from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from scriptRunner import ScriptRunner
import urlparse
from dummyScript import dummyScript
import json
from threading import Lock
from proxyUpdateFirmware11 import proxyUpdateFirmware11
from proxyDeleteApp import proxyDeleteApp

scripts = {
  "/dummy": dummyScript,
  "/install": proxyUpdateFirmware11, 
  "/uninstall": proxyDeleteApp,
}
runners = []

def findRunner(client):
  for runner in runners:
    if (runner.client == client):
      return runner
  return None

class ScriptRunnerWebsocketServer(WebSocket):

  def handleMessage(self):
    try:
      runner = findRunner(self)
      response = json.loads(self.data)
      if (runner != None and runner.nonce == response["nonce"]):
        runner.response = response
        runner.lock.release()
        runner.lock = Lock()
        runner.lock.acquire()
        print "Received " + self.data
    except: 
      pass

  def handleConnected(self):
    print "Connection " + self.request.path
    url = urlparse.urlparse(self.request.path)
    script = scripts[url.path]
    runner = findRunner(self)
    print runner
    if (script != None and runner == None):
      runner = ScriptRunner(self, script, urlparse.parse_qs(url.query))
      runners.append(runner)
      runner.start()
    elif (runner == None):
      self.close()

  def handleClose(self):
    runner = findRunner(self)
    if (runner != None):
      runner.lock.release()
      runners.remove(runner)
    print self.address, 'closed'

def run():
  server = SimpleWebSocketServer('', 3001, ScriptRunnerWebsocketServer)
  server.serveforever()


if __name__ == '__main__':
  run()