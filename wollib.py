import socket
from struct import pack

#wollib (Wake On Lan LIBrary) Version 1.02
#Copyright 2017,2018 Red Ponies A.F.
"""
 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
"""

#Variables par défaut
#Default vars
UDP_IP = "255.255.255.255"
UDP_PORT = 9

def wake(MAC):
	MACS = MAC.replace(":", "")
	DATA = "FFFFFFFFFFFF" + 16 * MACS
	#Test
	verif = len(MACS)
	vertxt = str(verif)
	print ("wollib: Address length : " + vertxt)
	if verif != 12 :
		print ("wollib: Address is wrong !")
		return("0")
	else:
		print("wollib: MAC address is : " + MACS)
		MESSAGE= b''
        
		#Sépare les valeurs hexa et les encode
		#Split vars and rewrite them
		for i in range(0, len(DATA), 2):
			MESSAGE = b''.join([MESSAGE, pack('B', int(DATA[i: i + 2], 16))])

		sock = socket.socket(socket.AF_INET, # Internet
							socket.SOCK_DGRAM) # UDP
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
		print ("wollib: Address correct, Magic Packet Send.")
		return("1")

def help():
    print ("Cette librairie Python 3 permet le réveil à distance d'un PC")
    print ("This Python 3 library can do WoL (yes)")
    print ("Syntaxe : wakelan.wake(MAC)")
