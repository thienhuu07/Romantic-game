import pygame
import random
import math
from pygame import mixer

pygame.init()

FPS = 60
fpsclock = pygame.time.Clock()

screen = pygame.display.set_mode((800,600))

# background
background = pygame.image.load('background.png')

# you
thienImg = []
thienX = []
thienY = []
thienX_change = []
thienY_change = []
num_of_thien = 5

for i in range(num_of_thien):
    thienImg.append(pygame.image.load('thien.png'))
    thienX.append(random.randint(0,735))
    thienY.append(random.randint(20,150))
    thienX_change.append(0.2)
    thienY_change.append(20)

    def thien(x,y,i):
        screen.blit(thienImg[i],(x,y))

# your girl friend
tuyenImg = pygame.image.load(tuyen.png')
tuyenX = 380
tuyenY = 500
tuyenX_change = 0
tuyenY_change = 0

def tuyen(x,y):
    screen.blit(tuyenImg,(x,y))

# heart
heartImg = pygame.image.load('heart.png')
heartX = 0
heartY = tuyenY
heartX_change = 0
heartY_change = 0.4

heart_state = "ready"

def heart(x,y):
    global heart_state
    heart_state = "fire"
    screen.blit(heartImg,(x+16,y+10))

# icon and title
title = pygame.display.set_caption("AnhYêuEm")
icon = pygame.image.load('heart.png')
pygame.display.set_icon(icon)

# check colision
def iscollision(thienX,thienY,heartX,heartY):
    distance = math.sqrt(math.pow(thienX - heartX,2)+math.pow(thienY - heartY,2))

    if distance < 27:
        return True
    else:
        return False

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Yêu Anh x " + str(score_value),True, (150,150,255))
    screen.blit(score,(x,y))

# Game over
over_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    over_text = over_font.render("You lost, but I still LOVE You!!!!!!" ,True, (150,150,255))
    screen.blit(over_text,(30,250))

# sound and music
mixer.music.load("cauhon.wav")
mixer.music.play(-1)

running = True
while running:

    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                tuyenX_change = 1
            if event.key == pygame.K_LEFT:
                tuyenX_change = -1
            if event.key == pygame.K_UP:
                tuyenY_change = -1
            if event.key == pygame.K_DOWN:
                tuyenY_change = 1
            if event.key == pygame.K_SPACE:
                if heart_state == "ready":
                    heartX = tuyenX
                    heartY = tuyenY
                    heart(heartX,heartY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                tuyenX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                tuyenY_change = 0

    tuyen(tuyenX,tuyenY)
    tuyenX += tuyenX_change
    tuyenY += tuyenY_change

    if tuyenX <=0:
        tuyenX = 0 
    elif tuyenX >=736:
        tuyenX = 736

    if tuyenY <= 400: 
        tuyenY = 400
    elif tuyenY >=530:
        tuyenY = 529

    for i in range(num_of_thien):
        # game over
        if thienY[i] > 200:
            for j in range(num_of_thien):
                thienY[j] =2000
            game_over_text()
            break

        thien(thienX[i],thienY[i],i)

        if thienX[i] <= 0:
            thienX_change[i] = 0.2
            thienY[i] += thienY_change[i]
        if thienX[i] >= 736:
            thienX_change[i] = -0.2
            thienY[i] += thienY_change[i]

        thienX[i] += thienX_change[i]
           
        collision = iscollision(thienX[i],thienY[i],heartX,heartY)
        if collision:
            heart_state = "ready"
            thienY[i] = random.randint(50,150)
            thienX[i] = random.randint(0,735)
            score_value += 1
            explosion_sound = mixer.Sound('tick.wav')
            explosion_sound.play()

    if heartY <= 0:
        heartY = tuyenY
        heart_state ="ready" 
    if heart_state == "fire":
        heartY -= heartY_change
        heart(heartX,heartY)

    show_score(textX,textY)
    fpsclock.tick()
    pygame.display.flip()
