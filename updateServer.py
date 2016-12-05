from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
from ledgerUpdateApi import LedgerUpdateAPI
import json
from urlparse import urlparse
from urlparse import parse_qs

api = LedgerUpdateAPI()

class LedgerUpdateHTTPRequestHandler(BaseHTTPRequestHandler):
	
	endpoints = {
		"/update/firmwares/last": api.getLastFirmware,
		"/update/firmwares": api.getFirmwares,
		"/update/applications": api.getApplications,
		"/update/devices": api.getDevices
	}

	assets = {
		"/update/assets/icons/": ('.png', 'image/png', './assets/icons/')
	}

	def handle_assets(self, path):
		url = urlparse(self.path)
		for key, value in self.assets.iteritems():
			print(key)
			print(path)
			print(path.startswith(key))
			print(value[2] + path.split('/')[-1] + value[0])
			if (path.startswith(key)):
				try:
					print(value[2] + path.split('/')[-1] + value[0])
					file = open(value[2] + path.split('/')[-1] + value[0], 'rb')
				 	self.send_response(200)
				 	self.send_header('Content-type', value[1])
				 	self.end_headers()
				 	self.wfile.write(file.read())
				 	file.close()
				except Exception as exception:
					answer = api.notFound(self, url.path, parse_qs(url.query))
					self.send_response(answer[0])
					self.send_header('Content-type','application/json')
					self.end_headers()
					self.wfile.write(json.dumps(answer[1]))
				return True
		return False

	def do_GET(self):
		url = urlparse(self.path)

		# Check if we request an asset first
		if (self.handle_assets(url.path) == False):
			#send code 200 response
			answer = self.endpoints.get(url.path, api.notFound)(self, url.path, parse_qs(url.query))
				
			self.send_response(answer[0])

			#send header first
			self.send_header('Content-type','application/json')
			self.end_headers()

			#send file content to client
			self.wfile.write(json.dumps(answer[1]))
		return

def run():
  print('http server is starting...')
  server_address = ('151.80.40.73', 3002)
  httpd = HTTPServer(server_address, LedgerUpdateHTTPRequestHandler)
  print('http server is running...')
  httpd.serve_forever()
  
if __name__ == '__main__':
  run()
