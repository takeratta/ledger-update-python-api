import struct

def dummyScript(dongle, params):
	targetid = bytearray(struct.pack('>I', 0x31000002)) # Blue
	targetid = bytearray(struct.pack('>I', 0x31100002)) # Nano S
	apdu = bytearray([0xe0, 0x04, 0x00, 0x00]) + bytearray([len(targetid)]) + targetid
	dongle.exchange(apdu)
