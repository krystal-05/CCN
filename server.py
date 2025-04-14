# Spongebob GameServer.py

import threading
import pygame
import socket
import sys
import random
import time

bucket_pos = [300, 350]
bucket_speed = 5
patties = []
score = 0
game_over = False
last_speed_increase = time.time()
speed_increase_interval = 10
speed_increment = 0.5

def load_image(filename, size=None):
	try:
		img = pygame.image.load(filename)
		if size:
			img = pygame.transform.scale(img, size)
		return img
	except:
		print(f"Error loading {filename}")
		sys.exit()

def game_thread():
	global bucket_pos, patties, score, game_over, bucket_speed, last_speed_increase
	pygame.init()
	screen_size = screen_width, screen_height = 600, 400
	screen = pygame.display.set_mode(screen_size)
	pygame.display.set_caption('Spongebob Bucket Catch')
	
	background = load_image('background.jpg', screen_size)
	bucket = load_image('bucket.jpg', (50, 50))
	patty = load_image('patty.jpg', (30, 30))

	fps.pygame.time.Clock()
	font = pygame.font.SysFont('arial', 24)

	last_spawn = time.time()
	spawn_interval = 2

	while True:
		if not game_over
			for event in pygame.event.get()
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
					bucket_pos = [300,350]
					patties = []
					score = 0
					bucket_speed = 5
					game_over = False
					last_speed_increase = time.time()

			if time.time() - last_spawn > spawn_interval:
				x = random.randint(0, screen_width - 30)
				patties.append([x, 0, 2])
				last_spawn = time.time()

			for p in patties[:]:
				p[1] += p[2]
				if p[1] > screen_height:
					game_over = True
					patties = []
					break
				bucket_rect = pygame.Rect(bucket_pos[0], bucket_pos[1], 50, 50)
				patty_rect = pygame.Rect(p[0], p[1], 30, 30)

				if bucket_rect.colliderect(patty_rect):
					score += 1
					patties.remove(p)

			if time.time() - last_speed_increase > speed_increase_interval:
				bucket_speed += speed_increment
				for p in patties:
					p[2] += speed_increment
				last_speed_increase = time.time()
		screen.blit(background, (0,0))
		if not game_over:
			screen.blit(bucket, bucket_pos)
			for p in patties:
				screen.blit(patty, (p[0], p[1]))
		else:
			game_over_text = font.render("Game over! Press 'r' to restart", True, (255, 0, 0))
			screen.blit(game_over_text, (screen_width // 2 - 150, screen_height // 2))
		score_text = font.render(f"Score: {score}", True, (0,0,0))
		screen.blit(score_text, (10, 10))

		pygame.display.update()
		fps.tick(60)

def server_thread():
	global bucket_pos, bucket_speed
	
	host = ''
	port = 5000

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((host, port))
	server_socket.listen(2)
	print("Server enabled, waiting for client...")

	conn, address = server_socket.accept()
	print(f"Connection from: {address}")

	while True:
		try:
			data = conn.recv(1024).decode()
			if not data:
				break
			if data == 'left' and bucket_pos[0] > 0:
				bucket_pos[0] -= bucket_speed
			elif data == 'right' and bucket_pos[0] < screen_width - 50:
				bucket_pos[0] += bucket_speed
			elif data == 'up' and bucket_pos[1] > 0:
				bucket_pos[1] -= bucket_speed
			elif data == 'down' and bucket_pos[1] < screen_height - 50:
				bucket_pos[1] += bucket_speed
		except:
			print("Client disconnected")
			break
	conn.close
	server_socket.close()

t1 = threading.Thread(target=game_thread)
t2 = threading.Thread(target=server_thread)
t1.start()
t2.start()
