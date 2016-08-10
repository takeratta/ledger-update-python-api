"""
*******************************************************************************
*   Ledger Blue
*   (c) 2016 Ledger
*
*  Licensed under the Apache License, Version 2.0 (the "License");
*  you may not use this file except in compliance with the License.
*  You may obtain a copy of the License at
*
*      http://www.apache.org/licenses/LICENSE-2.0
*
*  Unless required by applicable law or agreed to in writing, software
*  distributed under the License is distributed on an "AS IS" BASIS,
*  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
*  See the License for the specific language governing permissions and
*  limitations under the License.
********************************************************************************
"""

from secp256k1 import PrivateKey
from ledgerblue.deployed import getDeployedSecretV1, getDeployedSecretV2
from ledgerblue.hexLoader import HexLoader

def auto_int(x):
    return int(x, 0)

def proxyDeleteApp(dongle, args):
	args.targetId = auto_int(args.targetId)
	if args.appName == None:
		raise Exception("Missing appName")
	if args.targetId == None:
		args.targetId = 0x31000002
	if args.rootPrivateKey == None:
		privateKey = PrivateKey()
		publicKey = str(privateKey.pubkey.serialize(compressed=False)).encode('hex')
		print "Generated random root public key : " + publicKey
		args.rootPrivateKey = privateKey.serialize().encode('ascii')

	if args.deployLegacy:
		secret = getDeployedSecretV1(dongle, bytearray.fromhex(args.rootPrivateKey), args.targetId)
	else:
		secret = getDeployedSecretV2(dongle, bytearray.fromhex(args.rootPrivateKey), args.targetId)
	loader = HexLoader(dongle, 0xe0, True, secret)
	loader.deleteApp(args.appName)