
from pynput import keyboard
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

	def on_press(key):
		try:
			if key == keyboard.Key.left or key.char == 'a':
				client_socket.send('left'.encode())
			elif key == keyboard.Key.right or key.char == 'd':
				client_socket.send('right'.encode())
			elif key == keyboard.Key.up or key.char == 'w':
				client_socket.send('up'.encode())
			elif key == keyboard.Key.down or key.char == 's':
				client_socket.send('down'.encode())
			elif key.char == 'q':
				return False
		except AttributeError:
			pass
		except Exception as e:
			print(f"Server disconnected: {e}")
			return False
		
		time.sleep(0.05)

	with keyboard.Listener(on_press=on_press) as listener:
		listener.join()

	client_socket.close()
	print("Connection closed")

if __name__ == '__main__':
	client_program()
