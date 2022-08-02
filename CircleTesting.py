import pygame
from math import *
import numpy as np
import sys


width, height = 1000,1000
screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
pygame.display.set_caption("Circle testing")

point = (0,0)
radius = 1
a = 4
b = 5
scale = 50

def decimal_range(start, stop, step):

    while start <= stop:
        yield start
        start += step


points_donut = []
for x in (decimal_range(a * (-1), a, 0.05)):
    y = sqrt(pow(b, 2) - (pow(x, 2) / pow(a, 2) * pow(b, 2)))
    points_donut.append(np.matrix([x, y, 0]))
    new_y = y - dist((x, y), (x, 0)) * 2
    points_donut.append(np.matrix([x, new_y, 0]))

clock = pygame.time.Clock()
angle = 0

projection_matrix = np.matrix([
    [1,0,0],
    [0,1,0],
    [0,0,0]
])


# print(x)
# print(pow(x,2))
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    screen.fill((147, 125, 194))
    
    rotation_x = np.matrix([
        [1,0,0],
        [0,cos(angle), -sin(angle)],
        [0,sin(angle), cos(angle)]
    ])

    rotation_y = np.matrix([
        [cos(angle), 0,sin(angle)],
        [0,1,0],
        [-sin(angle), 0, cos(angle)]
    ])

    rotation_z = np.matrix([
        [cos(angle), -sin(angle),0],
        [sin(angle), cos(angle),0],
        [0,0,1]
    ])
    angle += 0.05

    for point in points_donut:
        rotate = np.dot(rotation_x,point.reshape((3,1)))
        rotate = np.dot(rotation_z,rotate)

        projected_point = np.dot(projection_matrix,rotate)

        # Get coordinates of each point, multiply with the scale to fit the screen,
        # add width//2 or height//2 to move shape to the middle of the screen

        x = int(projected_point[0][0] * 50) + width//2
        y = int(projected_point[1][0] * 50) + height//2

        # pygame.draw.circle(screen, (252, 197, 192), (x, y), radius, 10)
        pygame.draw.circle(screen, (252, 197, 192), (x, y), 100, 10)

    pygame.display.update()
