import sys
import argparse
import os
import struct
import urllib2, urlparse
from BlueHSMServer_pb2 import Request, Response, Parameter


def serverQuery(request, url, args):
	data = request.SerializeToString()
	url = urlparse.urlparse(args.url)
	req = urllib2.Request(args.url, data, {"Content-type": "application/octet-stream" })
	res = urllib2.urlopen(req)
	data = res.read()
	response = Response()
	response.ParseFromString(data)
	if len(response.exception) <> 0:
		raise Exception(response.exception)
	return response

def proxyUpdateFirmware11(dongle, args):

	# Identify

	targetid = bytearray(struct.pack('>I', 0x31000002)) # Blue
	targetid = bytearray(struct.pack('>I', 0x31100002)) # Nano S
	apdu = bytearray([0xe0, 0x04, 0x00, 0x00]) + bytearray([len(targetid)]) + targetid
	dongle.exchange(apdu)

	# Get nonce and ephemeral key

	request = Request()
	request.reference = "distributeFirmware11"
	parameter = request.remote_parameters.add()
	parameter.local = False
	parameter.alias = "persoKey"
	parameter.name = args.perso
	request.largeStack = True

	response = serverQuery(request, args.url, args)

	offset = 0

	remotePublicKey = response.response[offset : offset + 65]
	offset += 65
	nonce = response.response[offset : offset + 8]

	# Initialize chain 

	apdu = bytearray([0xe0, 0x50, 0x00, 0x00, 0x08]) + nonce
	deviceInit = dongle.exchange(apdu)
	deviceNonce = deviceInit[4 : 4 + 8]

	# Get remote certificate

	request = Request()
	request.reference = "distributeFirmware11"
	request.id = response.id
	parameter = request.remote_parameters.add()
	parameter.local = False
	parameter.alias = "persoKey"
	parameter.name = args.perso
	request.parameters = str(deviceNonce)
	request.largeStack = True

	response = serverQuery(request, args.url, args)

	offset = 0

	remotePublicKeySignatureLength = ord(response.response[offset + 1]) + 2
	remotePublicKeySignature = response.response[offset : offset + remotePublicKeySignatureLength]

	certificate = bytearray([len(remotePublicKey)]) + remotePublicKey + bytearray([len(remotePublicKeySignature)]) + remotePublicKeySignature
	apdu = bytearray([0xE0, 0x51, 0x80, 0x00]) + bytearray([len(certificate)]) + certificate
	dongle.exchange(apdu)

	# Walk the chain

	index = 0
	while True:
			if index == 0:
				certificate = bytearray(dongle.exchange(bytearray.fromhex('E052000000')))
			elif index == 1:
				certificate = bytearray(dongle.exchange(bytearray.fromhex('E052800000')))
			else:
					break
			if len(certificate) == 0:
				break
			request = Request()
			request.reference = "distributeFirmware11"
			request.id = response.id
			request.parameters = str(certificate)
			request.largeStack = True
			serverQuery(request, args.url, args)
			index += 1

	# Commit agreement and send firmware

	request = Request()
	request.reference = "distributeFirmware11"
	parameter = request.remote_parameters.add()
	parameter.local = False
	parameter.alias = "firmware"
	parameter.name = args.firmware
	parameter = request.remote_parameters.add()
	parameter.local = False
	parameter.alias = "firmwareKey"
	parameter.name = args.firmwareKey
	request.id = response.id
	request.largeStack = True

	response = serverQuery(request, args.url, args)
	responseData = bytearray(response.response)

	dongle.exchange(bytearray.fromhex('E053000000'))

	offset = 0 
	apdus = []
	while offset < len(responseData):
		apdu = responseData[offset : offset + 5 + responseData[offset + 4]]
		apdus.append(apdu)
		offset += 5 + responseData[offset + 4]
	dongle.bulkExchange(apdus)

