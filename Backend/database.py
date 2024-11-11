import socket
import sqlite3
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

# The key (must be 16 bytes)
key = b'Sixteen byte key'
port = 1235

# Create a socket
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 


# Associate the socket with the port
serverSock.bind(('', port)) 

# Start listening for incoming connections
serverSock.listen(4)

#Create a new database
conn = sqlite3.connect("userData.db")
#Create a cursor to traverse the database
cursor = conn.cursor()

cursor.execute('''
Create TABLE IF NOT EXISTS user(
    username TEXT PRIMARY KEY,
	password TEXT         
)
''')

# Keep accepting connections forever
while True:


	print("Waiting for clients to connect...")
	
		# Accept a waiting connection
	cliSock, cliInfo = serverSock.accept()
	
	print("Client connected from: " + str(cliInfo))
	
		# Receive the data the client has to send.
		# This will receive at most 1024 bytes
	data = cliSock.recv(1024)
	
	#Read IV
	iv = data[:AES.block_size]

	decCipher = AES.new(key, AES.MODE_CBC, iv)

	username_length = int.from_bytes(data[AES.block_size:AES.block_size + 4], "big")
	username_start = AES.block_size + 4
	username_end = username_start + username_length
	username_cipher = data[username_start:username_end]

	password_start = username_end + 4
	password_length = int.from_bytes(data[username_end:password_start], "big")
	password_end = password_start + password_length
	password_cipher = data[password_start:password_end]
	
	
	decrypted_username = unpad(decCipher.decrypt(username_cipher), AES.block_size).decode()
	decrypted_password = unpad(decCipher.decrypt(password_cipher), AES.block_size).decode()	
	
	print("Username: " + str(decrypted_username))
	print("Password: " + str(decrypted_password))

	try:
		cursor.execute('''INSERT INTO user (username, password) VALUES (?, ?)''', (str(decrypted_username), str(decrypted_password)))
		print("User data inserted into database :")
		data = cursor.execute('''SELECT * FROM user''')
		for row in data:
			print(row)
			conn.commit()

	except sqlite3.IntegrityError:
		print("Username already exists. Please try a different username")
	except Exception as error:
		print("An error occured: ", error)
		conn.close()
		cliSock.close()
	# Hang up the client's connection
	cliSock.close()
	
	