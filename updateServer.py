from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
from ledgerUpdateApi import LedgerUpdateAPI
import json

api = LedgerUpdateAPI()

class LedgerUpdateHTTPRequestHandler(BaseHTTPRequestHandler):
	
	endpoints = {
		"/update/firmwares/last": api.getLastFirmware,
		"/update/firmwares": api.getFirmwares,
		"/update/applications": api.getApplications,
	}

	def do_GET(self):
		#send code 200 response
		answer = self.endpoints.get(self.path, api.notFound)(self)
			
		self.send_response(answer[0])

		#send header first
		self.send_header('Content-type','application/json')
		self.end_headers()

		#send file content to client
		self.wfile.write(json.dumps(answer[1]))
		return

def run():
  print('http server is starting...')
  server_address = ('127.0.0.1', 3001)
  httpd = HTTPServer(server_address, LedgerUpdateHTTPRequestHandler)
  print('http server is running...')
  httpd.serve_forever()
  
if __name__ == '__main__':
  run()