import importlib
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad

keyUser = b'E8B6C00C9ADC5E75BB656ECD429CB1643A25B111FCD22C6622D53E0722439993'
keyAnotherUser = b'key=67BCB464EB033B8779F284186CB8996728BDC4C5F9DF58DE34497A82C2815E82'
sessionKey = b'C29B85EE8FA5A6D7E2805E4ACEC8A7E41883E8336891B23EFD5065F4FB6C6682'




moduleAlice = importlib.import_module("Alice")
myList = []
myList = moduleAlice.toKDC()
	
IDa = myList[0]
IDb = myList[1]
N1 = myList[2]

#Alice's Message
encCipherAlice = AES.new(masterAlice, AES.MODE_ECB)



encryptedAliceMessage = encCipherAlice.encrypt(pad(aliceNotEncryptedMessage, AES.block_size))


aliceEncryptedMessage = open("msg2a.txt.enc", "wb")
aliceEncryptedMessage.write(encryptedAliceMessage)
aliceEncryptedMessage.close()


#Another User's Message 
encCipherBob = AES.new(masterBob, AES.MODE_ECB)

bobMessage = open("msg2b.txt", "w")
bobMessage.write(str([IDa, sessionKey]))
bobMessage.close()

bobMessage = open("msg2b.txt", "rb")
bobNotEncryptedMessage = bobMessage.read()
bobMessage.close()

encryptedBobMessage = encCipherBob.encrypt(pad(bobNotEncryptedMessage, AES.block_size))

bobEncryptedMessage = open("msg2b.txt.enc", "wb")
bobEncryptedMessage.write(encryptedBobMessage)
bobEncryptedMessage.close()



#Sending Alice her message that she will send to Bob
def forAlice():
	aliceMessage = open("msg2a.txt.enc", "rb")
	bobMessage = open("msg2b.txt.enc", "rb")
	#aliceList = []
	#bobList = []
	#myList= []
	
	#print(type(aliceList))
	#for line in aliceMessage:
	#	aliceList.append(line)
	#for line in bobMessage:
	#	bobList.append(line)
	#myList = [aliceList, "|", bobList]
	return aliceMessage.readlines(), bobMessage.readlines()

if __name__ == '__main__':
	forAlice()
	print("KDC running")
	print("I run forAlice()")

mylist = forAlice()

print(mylist)
