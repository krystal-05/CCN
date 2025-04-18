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
screen_width, screen_height = 600, 400

#load button images(not made yet)
start_img = pygame.image.load('start_btn.png') 
exit_img = pygame.image.load('exit_btn.png')
restart_img = pygame.image.load('restart_btn.png')
menu_img = pygame.image.load('menu_btn.png')

#button class for start/quit/restart game and main menu
class Button():
    #constructor
    def __init__ (self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width * scale), int(height * scale)))
        #maybe scaling will help the bucket issue 
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False 

    #draw buttons on screen
    def draw(self, surface):
        action = False 
        #get mouse position 
        pos = pygame.mouse.get_pos()

        #check if mouse is over a button 
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: ##if leftmost button is clicked
                self.clicked = True
                action = True 
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #blit transfers image onto the screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

#create button instances 
#scale values may need to change 
start_button = Button(100, 200, start_img, 0.8) 
exit_button = Button(200, 200, exit_img, 0.8)
restart_button = Button(300, 200, restart_img, 0.8)
menu_button = Button(400, 300, menu_img, 0.8)
pause_button = Button(400, 300, menu_img, 0.8)


def load_image(filename, size=None):
	try:
		img = pygame.image.load(filename)
		if size:
			img = pygame.transform.scale(img, size)
		return img
	except Exception as e:
		print(f"Error loading {filename}: {e}")
		sys.exit()

def main_menu():
    pygame.init()
    screen_size = screen_width, screen_height = 600, 400
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Spongebob Bucket Catch - Main Menu')
    menuBackground = load_image('field.png', screen_size)

    while True:
        screen.blit(menuBackground, (0, 0))

        if start_button.draw(screen):
            return game_thread()


def game_thread():
	global bucket_pos, patties, score, game_over, bucket_speed, last_speed_increase
	pygame.init()
	screen_size = screen_width, screen_height = 600, 400
	screen = pygame.display.set_mode(screen_size)
	pygame.display.set_caption('Spongebob Bucket Catch')
	
	background = load_image('field.png', screen_size)
	bucket = load_image('bucket.png', (50, 50))
	patty = load_image('patty1.png', (30, 30))
	fps = pygame.time.Clock()
	font = pygame.font.SysFont('arial', 24)
	last_spawn = time.time()
	spawn_interval = 2

	while True:
		if not game_over:
			for event in pygame.event.get():
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
			exit_button.draw()
			restart_button.draw()
			menu_button.draw()
			pygame.quit()
			sys.exit()
		score_text = font.render(f"Score: {score}", True, (0,0,0))
		screen.blit(score_text, (10, 10))
		pygame.display.update()
		fps.tick(60)

def server_thread():
	global bucket_pos, bucket_speed, screen_width, screen_height
	
	host = '10.22.0.42'
	port = 5001
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
				bucket_pos[1] += bucket_speed
		except Exception as e:
			print(f"Client disconnected: {e}")
			break

	conn.close()
	server_socket.close()
   
#I think the reason the game is crashing when its over is because we dont have pygame.quit().
#This handles the networking and closes the connection with the server but we need to close the game window.

if __name__ == "__main__":
    t2 = threading.Thread(target=server_thread)  # server in background
    t2.start()
    main_menu()


# Check to see if button and main menu functionality works
# Rest of need-to-do list needs to be implemented, will do over weekend