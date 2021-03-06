import pygame
import random
import sys

pygame.init()

pygame.display.set_caption("retrogun")

gameFont = pygame.font.SysFont("None", 23)
menuFont = pygame.font.SysFont("Serif", 44)

shootSound = pygame.mixer.Sound("sounds/shoot.wav")
backgroundSound = pygame.mixer.Sound("sounds/background.wav")

shape = pygame.image.load('images/game-controller.png')
shape = pygame.transform.scale(shape, (180, 190))

enemy = pygame.image.load('images/character.png')
enemy = pygame.transform.scale(enemy, (70, 70))

black = 0, 0, 0
white = 200, 200, 200

shapeX, shapeY = 180, 500

circleX = 0
circleY = 0

screen = pygame.display.set_mode([800, 700])


def player(x, y):
    screen.blit(shape, (x, y))


def drawCircle(x, y, diameter, color=(255, 0, 0)):
    pygame.draw.circle(screen, color, [x, y], diameter, 5)


def createCircle(shapeX, shapeY, circles):
    circleX = shapeX + 70
    circleY = shapeY - 20
    diameter = 10
    r = random.randint(120, 255)
    g = random.randint(120, 255)
    b = random.randint(120, 255)
    circles.append([circleX, circleY, diameter, (r, g, b)])


def createEnemy(enemyX, enemyY):
    screen.blit(enemy, (enemyX, enemyY))


def checkCollision(x1, y1, x2, y2, w1, h1, w2, h2):
    xColl = False
    yColl = False

    if x1 + w1 >= x2 and x1 <= x2 + w2:
        xColl = True
    if y1 + h1 >= y2 and y1 <= y2 + h2:
        yColl = True

    if xColl and yColl:
        return 1
    return 0


def mainMenu():
    while True:
        pygame.mixer.Sound.play(backgroundSound)
        pygame.mixer.Sound.set_volume(backgroundSound, 0.009)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game(shapeX, shapeY)

        screen.fill(black)
        pygame.draw.rect(screen, (65, 96, 120), [175, 200, 450, 70])
        startMsg = menuFont.render("PRESS ENTER FOR START", 1, (255, 255, 255))
        screen.blit(startMsg, (200, 220))


        pygame.display.update()


def game(shapeX, shapeY):

    velocity = 3
    enemyVelocity = 1
    circles = []
    enemyX, enemyY = 40, 70
    enemyHealth = 100

    while enemyHealth > 0:
        screen.fill(black)
        health = gameFont.render("HP: " + str(enemyHealth), 1, (255, 255, 255))
        screen.blit(health, (30, 30))

        pygame.mixer.Sound.play(backgroundSound)
        pygame.mixer.Sound.set_volume(backgroundSound, 0.01)

        msg = gameFont.render("PRESS ENTER TO SHOOT", 1, (255, 255, 255))
        screen.blit(msg, (560, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.Sound.play(shootSound)
                    createCircle(shapeX, shapeY, circles)

        shapeX += velocity
        enemyX += enemyVelocity

        for circle in circles:
            i = 0
            drawCircle(circle[0], circle[1], circle[2], color=circle[3])
            circle[1] -= 7
            circle[2] += 0.4
            if circle[1] < -10:
                circles.pop(0)

            if checkCollision(circle[0], circle[1], enemyX, enemyY, 10, 10, 70, 70):
                circles.pop(circles.index(circle))
                enemyHealth -= 5
            i += 1

        if shapeX > 570 or shapeX < 20:
            velocity *= -1

        if enemyX > 570 or enemyX < 20:
            enemyVelocity *= -1

        createEnemy(enemyX, enemyY)
        player(shapeX, shapeY)

        pygame.display.update()

mainMenu()