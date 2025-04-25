import threading
import pygame
import socket
import sys
import random
import time

#These are the game settings
screen_width, screen_height = 1200, 720
bucket_size = (300, 300)
patty_size = (200, 200)
bucket_collision_size = (int(bucket_size[0] * 0.5), int(bucket_size[1] * 0.5))
patty_collision_size = (int(patty_size[0] * 0.3), int(patty_size[1] * 0.3))
bucket_speed = 50
min_x = 0
max_x = screen_width - bucket_size[0]
min_y = 0
max_y = screen_height - bucket_size[1]
bucket_pos = [screen_width // 2 - bucket_size[0] // 2, screen_height - bucket_size[1]]
patties = []
score = 0
state = 'start'
last_speed_increase = time.time()
speed_increase_interval = 0.7
speed_increment = 2.0

def load_image(filename, size=None):
    try:
        img = pygame.image.load(filename)
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        sys.exit()

def start_game():
    global state, bucket_pos, patties, score, last_speed_increase, last_spawn
    print("Starting game: Transitioning to the 'playing' state")
    state = 'playing'
    bucket_pos = [screen_width // 2 - bucket_size[0] // 2, screen_height - bucket_size[1]]
    patties = []
    score = 0
    last_speed_increase = time.time()
    last_spawn = time.time()

def game_thread():
    global bucket_pos, patties, score, state, bucket_speed, last_speed_increase, last_spawn
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Spongebob Bucket Catch')

    background = load_image('field.png', (screen_width, screen_height))
    bucket = load_image('bucket.png', bucket_size)
    patty = load_image("patty1.png", patty_size)
    fps = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 48)
    last_spawn = time.time()
    spawn_interval = 2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if state == 'playing':
            # This controls spawning the patties
            if time.time() - last_spawn > spawn_interval:
                x = random.randint(0, screen_width - patty_size[0])
                patties.append([x, 50, 3])
                last_spawn = time.time()

            # This moves the patties and checks if the game should be over
            for p in patties[:]:
                p[1] += p[2]
                if p[1] > screen_height:
                    print("Patty missed, game over")
                    state = 'game_over'
                    break

                # This controls collision detection
                bucket_rect = pygame.Rect(
                    bucket_pos[0] + (bucket_size[0] - bucket_collision_size[0]) // 2,
                    bucket_pos[1] + (bucket_size[1] - bucket_collision_size[1]) // 2,
                    bucket_collision_size[0],
                    bucket_collision_size[1]
                )
                patty_rect = pygame.Rect(
                    p[0] + (patty_size[0] - patty_collision_size[0]) // 2,
                    p[1] + (patty_size[1] - patty_collision_size[1]) // 2,
                    patty_collision_size[0],
                    patty_collision_size[1]
                )
                if bucket_rect.colliderect(patty_rect):
                    score += 1
                    patties.remove(p)
                
            # This controls the increase in speed
            if time.time() - last_speed_increase > speed_increase_interval:
                bucket_speed += speed_increment
                for p in patties:
                    p[2] += speed_increment
                last_speed_increase = time.time()

        # This handles rendering
        screen.blit(background, (0, 0))
        if state == 'playing':
            screen.blit(bucket, bucket_pos)
            for p in patties:
                screen.blit(patty, (p[0], p[1]))
        elif state == 'start':
            start_text = font.render("Waiting for the player to press 'r' to start", True, (0, 0, 0))
            screen.blit(start_text, (screen_width // 2 - 400, screen_height // 2 - 50))
        elif state == 'game_over':
            game_over_text = font.render("Game over! Player can press 'r' to restart", True, (255, 0, 0))
            screen.blit(game_over_text, (screen_width // 2 - 300, screen_height // 2 - 50))
        
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        pygame.display.update()
        fps.tick(60)

def server_thread():
    global bucket_pos, bucket_speed, state
    host = ''
    port = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    print("Server enabled, waiting for the client...")

    conn, address = server_socket.accept()
    print(f"Connection from: {address}")

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            if data == 'left' and bucket_pos[0] > min_x:
                bucket_pos[0] -= bucket_speed
            elif data == 'right' and bucket_pos[0] < max_x:
                bucket_pos[0] += bucket_speed
            elif data == 'up' and bucket_pos[1] > min_y:
                bucket_pos[1] -= bucket_speed
            elif data == 'down' and bucket_pos[1] < max_y:
                bucket_pos[1] += bucket_speed
            elif data == 'start':
                if state == 'start' or state == 'game_over':
                    start_game()
        except Exception as e:
            print(f"Client disconnected: {e}")
            break

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    t1 = threading.Thread(target=game_thread)
    t2 = threading.Thread(target=server_thread)
    t1.start()
    t2.start()
