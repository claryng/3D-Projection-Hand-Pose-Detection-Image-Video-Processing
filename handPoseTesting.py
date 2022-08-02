import mediapipe as mp
import cv2
import pygame as pg
import sys
import numpy as np


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

screen = pg.display.set_mode((1000,1000),pg.RESIZABLE)
pg.display.set_caption("Testing")

with mp_hands.Hands(max_num_hands=2,min_detection_confidence=0.7,min_tracking_confidence=0.5) as hands:

    video = cv2.VideoCapture(0)

    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    pg.quit()
                    sys.exit()

        # SCREEN PYGAME
        screen.fill((223, 246, 255))

        pg_img = pg.image.tostring(screen,"RGB")

        temp_surface = pg.image.fromstring(pg_img,(1000,1000),"RGB")

        temp_surface_array = pg.surfarray.array3d(temp_surface)

        # print(temp_surface_array)

        # HAND POSE DETECTION AND TRACKING
        check, frame = video.read()

        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        image.flags.writeable = False

        landmarks = hands.process(image)

        image.flags.writeable = True

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if landmarks.multi_hand_landmarks:
            for hand in landmarks.multi_hand_landmarks:
                mp_drawing.draw_landmarks(temp_surface_array,hand,mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec((6, 40, 61),thickness=5,circle_radius=5),
                                          mp_drawing.DrawingSpec((19, 99, 223), thickness=5,circle_radius=3))

        # screen.blit(pg.transform.rotate(pg.transform.scale(pg.surfarray.make_surface(temp_surface_array),(500,500)),-90.00),(200,200))
        screen.blit(pg.transform.rotate(pg.surfarray.make_surface(temp_surface_array),-90.0),(0,0))

        # cv2.imshow("testing",image)
        #
        # key = cv2.waitKey(10)
        #
        # if key == ord('q'):
        #     break

        pg.display.update()
    video.release()
    cv2.destroyAllWindows()
