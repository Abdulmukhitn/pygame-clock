import pygame
import sys
import time
import datetime
import os
import random
import math

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Clock")
font = pygame.font.Font(None, 36)
icon= pygame.image.load("image.png")
pygame.display.set_icon(icon)

image = pygame.image.load("clock.png")
imageX = 0
imageY = 0

minute_h = pygame.image.load("min_hand.png")
minuteX = 0
minuteY = 0

second_h = pygame.image.load("sec_hand.png")
secondX = 0
secondY = 0

center_x, center_y = 400, 300

LENGTH_MINUTE = 100
LENGTH_SECOND = 120

def draw_hand(image, angle, length):
    rotated_hand = pygame.transform.rotate(image, -angle) 
    rect = rotated_hand.get_rect(center=(center_x, center_y))  
    screen.blit(rotated_hand, rect.topleft)


def clock ():
    screen.blit(image, (imageX, imageY))

def minute():
    screen.blit(minute_h, (minuteX, minuteY))

def second():
    screen.blit(second_h, (secondX, secondY))
    

done=False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
    pygame.display.flip()
    screen.fill((192,100,192))
    clock()

    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    minutea = now.minute
    seconda = now.second

    minute_angle = minutea * 6 + (seconda / 60) * 6
    second_angle = seconda * 6

    draw_hand(minute_h, minute_angle, LENGTH_MINUTE)
    draw_hand(second_h, second_angle, LENGTH_SECOND)
    pygame.display.flip()
    pygame.time.delay(10)
