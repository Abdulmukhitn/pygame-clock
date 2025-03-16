import pygame
import sys
import datetime
import os
import math

pygame.init()
pygame.mixer.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Combined App")
clock = pygame.time.Clock()

current_dir = os.path.dirname(os.path.abspath(__file__))


try:
    clock_bg = pygame.image.load(os.path.join(current_dir, "clock.png")).convert_alpha()
    minute_hand = pygame.image.load(os.path.join(current_dir, "min_hand.png")).convert_alpha()
    second_hand = pygame.image.load(os.path.join(current_dir, "sec_hand.png")).convert_alpha()
except pygame.error as e:
    print(f"Error loading images: {e}")
    print("Make sure clock.png, min_hand.png, and sec_hand.png are in the same directory as this script")
    pygame.quit()
    sys.exit()

clock_center = (screen_width//2, screen_height//4)

ball_radius = 25
ball_pos = [screen_width//2, screen_height*3//4]
ball_speed = 20

music_tracks = ["track1.mp3", "track2.mp3", "track3.mp3"]
full_music_paths = [os.path.join(current_dir, track) for track in music_tracks]
current_track = 0
paused = False
music_loaded = False

def draw_clock_hand(image, angle, pivot):
    rotated = pygame.transform.rotate(image, -angle)
    rect = rotated.get_rect(center=pivot)
    return rotated, rect

def handle_music_controls(key):
    global current_track, paused, music_loaded
    
    if key == pygame.K_p:
        if not music_loaded:
            try:
                pygame.mixer.music.load(full_music_paths[current_track])
                pygame.mixer.music.play()
                music_loaded = True
                paused = False
                print(f"Playing: {music_tracks[current_track]}")
            except pygame.error as e:
                print(f"Error loading music: {e}")
                print(f"Tried to load: {full_music_paths[current_track]}")
        elif paused:
            pygame.mixer.music.unpause()
            paused = False
            print("Music unpaused")
        else:
            pygame.mixer.music.pause()
            paused = True
            print("Music paused")
            
    elif key == pygame.K_s:
        pygame.mixer.music.stop()
        paused = False
        music_loaded = False
        print("Music stopped")
        
    elif key == pygame.K_n:
        current_track = (current_track + 1) % len(music_tracks)
        try:
            pygame.mixer.music.load(full_music_paths[current_track])
            pygame.mixer.music.play()
            music_loaded = True
            paused = False
            print(f"Playing next: {music_tracks[current_track]}")
        except pygame.error as e:
            print(f"Error loading next track: {e}")
            
    elif key == pygame.K_b:
        current_track = (current_track - 1) % len(music_tracks)
        try:
            pygame.mixer.music.load(full_music_paths[current_track])
            pygame.mixer.music.play()
            music_loaded = True
            paused = False
            print(f"Playing previous: {music_tracks[current_track]}")
        except pygame.error as e:
            print(f"Error loading previous track: {e}")

def handle_ball_movement(key):
    if key == pygame.K_LEFT and ball_pos[0] > ball_radius + ball_speed:
        ball_pos[0] -= ball_speed
    elif key == pygame.K_RIGHT and ball_pos[0] < screen.get_width() - ball_radius - ball_speed:
        ball_pos[0] += ball_speed
    elif key == pygame.K_UP and ball_pos[1] > ball_radius + ball_speed:
        ball_pos[1] -= ball_speed
    elif key == pygame.K_DOWN and ball_pos[1] < screen.get_height() - ball_radius - ball_speed:
        ball_pos[1] += ball_speed

def recenter_elements():
    global clock_center, ball_pos
    clock_center = (screen.get_width()//2, screen.get_height()//4)
    ball_pos = [screen.get_width()//2, screen.get_height()*3//4]

missing_tracks = []
for track_path in full_music_paths:
    if not os.path.exists(track_path):
        missing_tracks.append(os.path.basename(track_path))

if missing_tracks:
    print(f"Warning: The following music tracks are missing: {', '.join(missing_tracks)}")
    print(f"Make sure these files are in the same directory as this script: {current_dir}")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_p, pygame.K_s, pygame.K_n, pygame.K_b]:
                handle_music_controls(event.key)
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                handle_ball_movement(event.key)
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            recenter_elements()

    now = datetime.datetime.now()
    minutes = now.minute
    seconds = now.second

    minute_angle = (minutes * 6) + (seconds / 10) - 90
    second_angle = (seconds * 6) - 90

    screen.fill((255, 255, 255))
    
    screen.blit(clock_bg, (clock_center[0] - clock_bg.get_width()//2, 
                          clock_center[1] - clock_bg.get_height()//2))
    
    min_hand, min_rect = draw_clock_hand(minute_hand, minute_angle, clock_center)
    sec_hand, sec_rect = draw_clock_hand(second_hand, second_angle, clock_center)
    screen.blit(min_hand, min_rect)
    screen.blit(sec_hand, sec_rect)
    
    pygame.draw.circle(screen, (255, 0, 0), [int(ball_pos[0]), int(ball_pos[1])], ball_radius)
    
    font = pygame.font.Font(None, 24)
    status_text = [
        f"Now Playing: {music_tracks[current_track]}" + (" (Paused)" if paused else ""),
        "Controls: P=Play/Pause, S=Stop, N=Next, B=Previous",
        "Ball Controls: Arrow Keys"
    ]
    for i, text in enumerate(status_text):
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (10, 10 + i*25))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()