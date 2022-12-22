#!/usr/bin/env python3
# coding: utf-8
# - utilisation encodage sha256: https://youtu.be/j9fO9-59EdI
# - récupération adresse mac : https://www.security-helpzone.com/2014/12/27/gnu-linux-debian-systeme-recuperer-ladresse-mac-sous-linux/
# - supression retour à la ligne: https://www.delftstack.com/fr/howto/python/python-remove-newline-from-string/

from hashlib import sha256
import os, sys

def GenerateCryptedKey():
	InitialKey		= os.popen("cat /sys/class/net/$(ip route show default | awk '/default/ {print $5}')/address").read()
	InitialKey		= InitialKey.strip()
	return(sha256(InitialKey.encode('utf-8')).digest())
	

def Crypt(CryptedFile,InitialValue):
	CryptedKey		= GenerateCryptedKey()
	with open(CryptedFile,'wb') as F_Crypted:
		I = 0
		while I < len(InitialValue):
			Character	= ord(InitialValue[I])
			Modulo		= I % len(CryptedKey)
			F_Crypted.write(bytes([Character^CryptedKey[Modulo]]))
			I+=1

def Uncrypt(CryptedFile):
	CryptedKey		= GenerateCryptedKey()
	InitialValue	= ''
	with open(CryptedFile,'rb') as F_Crypted:
		I = 0
		while F_Crypted.peek():
			Character	= ord(F_Crypted.read(1))
			Modulo		= I % len(CryptedKey)
			Byte = bytes([Character^CryptedKey[Modulo]])
			Byte = Byte.decode('utf-8')
			InitialValue=InitialValue+Byte
			I+=1
	return(InitialValue)

if __name__ == '__main__':
	NbArg = len(sys.argv)
	if NbArg != 3:
		print('Crypt[Error] not enough arguments')
	else:
		P1=sys.argv[1]
		P2=sys.argv[2]
		Crypt(P1,P2)
