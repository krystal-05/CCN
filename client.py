# Spongebob GameClient.py

import pynput
import socket
import time

def client_program():
	print("Trying to connect to server...")
	host = "x.x.x.x"
	port = 5000

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		client_socket.connect((host,port))
		print("Connected to server")
	except Exception as e:
		print(f"Connection failed: {e}")
		return

	print("Use WASD or arrow keys to move the bucket. Press 'q' to quit.")

	while True:
		if keyboard.is_pressed('q'):
			break
		keys = {
			'left': keyboard.is_pressed('left') or keyboard.is_pressed('a'),
			'right': keyboard.is_pressed('right') or keyboard.is_pressed('d'),
			'up': keyboard.is_pressed('up') or keyboard.is_pressed('w'),
			'down': keyboard.is_pressed('down') or keyboard.is_pressed('d')
		}

		for key, pressed in keys.item():
			if pressed:
				try:
					client_socket.send(key.encode())
				except:
					print("Server disconnected")
					client_socket.close()
					return
				time.sleep(0.05)
	client_socket.close()
	print("Connection closed")

if __name__ == '__main__':
	client_program()

	
