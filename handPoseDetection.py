# Import packages
import mediapipe as mp
import cv2
import numpy as np
from imutils import resize
import os
import uuid
import keyboard
import pygame
import sys
from math import *


# Set up screen
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
pygame.display.set_caption("Testing")

# Vertice of the 3D shapes
points = [
    np.matrix([0,3,0]),
    np.matrix([1,1,0]),
    np.matrix([3,2,0]),
    np.matrix([1.5,0,0]),
    np.matrix([3,-2,0]),
    np.matrix([1,-1,0]),
    np.matrix([0,-3,0]),
    np.matrix([-1,-1,0]),
    np.matrix([-3,-2,0]),
    np.matrix([-1.5,0,0]),
    np.matrix([-3,2,0]),
    np.matrix([-1,1,0]),

    np.matrix([0, 3, 3]),
    np.matrix([1, 1, 3]),
    np.matrix([3, 2, 3]),
    np.matrix([1.5, 0, 3]),
    np.matrix([3, -2, 3]),
    np.matrix([1, -1, 3]),
    np.matrix([0, -3, 3]),
    np.matrix([-1, -1, 3]),
    np.matrix([-3, -2, 3]),
    np.matrix([-1.5, 0, 3]),
    np.matrix([-3, 2, 3]),
    np.matrix([-1, 1, 3])
]

# Angle of rotation
angle = 0

# Clock to control framerate
clock = pygame.time.Clock()

# Projection matrix to project 3d onto 2d screen
projection_matrix = np.matrix([
    [1,0,0],
    [0,1,0],
    [0,0,0]
])

# Create a list of length of sum of vertice of the shape to store 2d projected points
projected_points = [
    [n,n] for n in range(len(points))
]

# Scale to increase or decrease the size of the shape
scale = 100


# Connect the dots with lines
def connection(point, a, b):
    pygame.draw.line(screen, (244, 124, 124), (point[a][0],point[a][1]),(point[b][0],point[b][1]),3)


# Drawing utilities to draw hand landmarks
mp_drawing = mp.solutions.drawing_utils

# hands module to get Hand Object
mp_hands = mp.solutions.hands

# Create frontal-face object
face_object = cv2.CascadeClassifier("Files/haarcascade_frontalface_default.xml")

# Save images
if keyboard.is_pressed('s'):
    # Create a folder to save images from cam
    os.mkdir('Outputs')


# Get the label of the hand: left or right
def get_label(ind, hand, landmarks):

    output = None

    # Check the index of the detected hand
    for classification in landmarks.multi_handedness:

        if classification.classification[0].index == ind:
            # Get label: left or right
            label = classification.classification[0].label

            # Score of estimated handedness
            score = round(classification.classification[0].score, 2)

            text_str = f"{label} {score}"

            # coordinates of the Wrist to later display text at that position
            coords = tuple(np.multiply(
                np.array((hand.landmark[mp_hands.HandLandmark.WRIST].x, hand.landmark[mp_hands.HandLandmark.WRIST].y)),
                [500, 500]
            ).astype(int))

            output = text_str, coords

    return output


# Update scale when shape NOT rotating
def update_scale(points):

    for i,point in enumerate(points):
        x = ((point[0] - width//2)/100) * scale + width//2
        y = ((point[1] - height//2)/100) * scale + height//2
        projected_points[i] = [x,y]


# Count fingers
def fingers_count(hand, handedness):

    # Store 1 or 0 (length 5)
    # 1 means open, 0 means close
    fingers = []

    # Left vs Right matters to the THUMB only
    # Check the THUMB first
    # Right hand
    if handedness == "Right":

        # When palm faces screen
        if hand.landmark[5].x < hand.landmark[9].x:

            # Check the x coordinates of tip of thumb and middle joint of thumb
            # if tip's x is smaller than that of middle joint, then thumb is opened
            if hand.landmark[4].x < hand.landmark[3].x:
                fingers.append(1)
            else:
                fingers.append(0)

        # When the palm faces the other way
        else:
            # if tip's x is greater than that of middle joint, then thumb is opened
            if hand.landmark[4].x > hand.landmark[3].x:
                fingers.append(1)
            else:
                fingers.append(0)

    # Left hand
    else:

        # When palm faces screen
        if hand.landmark[5].x > hand.landmark[9].x:
            if hand.landmark[4].x > hand.landmark[3].x:
                fingers.append(1)
            else:
                fingers.append(0)

        # When palm does not face the screen
        else:
            if hand.landmark[4].x < hand.landmark[3].x:
                fingers.append(1)
            else:
                fingers.append(0)

    for i in range(8, 21, 4):
        if hand.landmark[i].y < hand.landmark[i-2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)


with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.8, min_tracking_confidence=0.6) as hands:
    video = cv2.VideoCapture(0)

    # This flag represents initial frame when the shape is NOT moving
    flag = False

    # This flag shows if the shape is currently moving or not
    rotating = False

    # When capturing the video
    while video.isOpened():

        # framerate
        clock.tick(60)

        # Close windows
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        # Fill screen
        screen.fill((255, 231, 191))

        # Label of detected hand to later on control the rotation of the shape
        hand_indicator = None

        # Read the frame
        check, frame = video.read()

        # Resize the frame
        frame = resize(frame,width=500, height=500)

        # Convert from BGR to RGB to use process method of Hand object in mediapipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # flip the frame about the y-axis
        image = cv2.flip(image, 1)

        # face detection
        face_detection = face_object.detectMultiScale(frame, scaleFactor=1.05, minNeighbors=7)

        # set writeable flags to False so that we can process the frame without writing on it
        image.flags.writeable = False

        # detect landmarks
        landmarks = hands.process(image)

        # set flags back to writeable
        image.flags.writeable = True

        # Change back to BGR color
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # for x, y, w, h in face_detection:
        #     cv2.rectangle(image,(x,y),(x+w,y+h),(179,129,238),3)
        #     cv2.putText(image,text="Face",org=(x + x//3,y+h + h//6),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=2,color=(85,9,129),thickness=3)

        # Draw hand landmarks, get hand label
        if landmarks.multi_hand_landmarks:

            for hand in landmarks.multi_hand_landmarks:

                # draw landmarks
                mp_drawing.draw_landmarks(image,hand,mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(85,9,129), thickness=2,circle_radius=6),
                                          mp_drawing.DrawingSpec(color=(179,129,238),thickness=2,circle_radius=3))

                # get index of current detected hand
                index = landmarks.multi_handedness[0].classification[0].index

                # Put text: label of the hand
                if get_label(index,hand, landmarks):
                    text, coordinates = get_label(index,hand, landmarks)
                    cv2.putText(image, text,coordinates,fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(85,9,129),thickness=3)

                    # Re-assign hand label to control shape's rotation
                    hand_indicator = text[:5]

                    fingers_count(hand,hand_indicator[:4 if hand_indicator == "Left " else 5])

        # rotation matrix
        rotation_x = np.matrix([
            [1, 0, 0],
            [0, cos(angle), -sin(angle)],
            [0, sin(angle), cos(angle)]
        ])

        rotation_y = np.matrix([
            [cos(angle), 0, sin(angle)],
            [0, 1, 0],
            [-sin(angle), 0, cos(angle)]
        ])

        rotation_z = np.matrix([
            [cos(angle), -sin(angle), 0],
            [sin(angle), cos(angle), 0],
            [0, 0, 1]
        ])

        # Update angle of rotation
        angle += 0.01

        # Increase shape's size
        if keyboard.is_pressed('i'):
            scale += 10
            if not rotating:
                update_scale(projected_points)

        # Decrease shape's size
        if keyboard.is_pressed('d'):
            scale -= 10
            if not rotating:
                update_scale(projected_points)

        # Projection onto 2d screen
        for i, point in enumerate(points):

            if hand_indicator:
                # If right hand detected or pressing r, rotate about x-, y-, and then z-axis
                if hand_indicator == "Right" or keyboard.is_pressed('r'):

                    # Rotate each point
                    rotate = np.dot(point, rotation_x)
                    rotate = np.dot(rotate, rotation_y)
                    rotate = np.dot(rotate, rotation_z)

                # if left hand deteced or pressing l key, rotate about the z-, y-, x- axis
                elif hand_indicator == "Left " or keyboard.is_pressed('l'):

                    # rotate each point
                    rotate = np.dot(point, rotation_z)
                    rotate = np.dot(rotate, rotation_y)
                    rotate = np.dot(rotate, rotation_x)

                # Project onto 2d screen
                projected_point = np.dot(rotate, projection_matrix).reshape(3, 1)

                # Get coordinates of each point, multiply with the scale to fit the screen,
                # add width//2 or height//2 to move shape to the middle of the screen
                x = int(projected_point[0][0] * scale) + width // 2
                y = int(projected_point[1][0] * scale) + width // 2

                # set flag to True so that if user wants to stop rotating
                # the shape would stay at that current state
                flag = True

                # Get the updated coordinates
                projected_points[i] = [x, y]

                # Draw the vertice
                pygame.draw.circle(screen, (161, 0, 53), (x, y), 5, 5)

                # Set rotating to True
                rotating = True

            # if no indicators to rotate:
            else:

                # initial set up of the shape before any rotations
                if not flag:
                    point = point.reshape((3, 1))
                    x = int(point[0][0] * scale) + width // 2
                    y = int(point[1][0] * scale) + width // 2

                    projected_points[i] = [x, y]

                    pygame.draw.circle(screen, (161, 0, 53), (x, y), 5, 5)

                # set rotation flag to False to update scale if indicated
                rotating = False

        # connect the lines of the shape
        for i in range(len(projected_points)):

            connection(projected_points, i, (i + 1 if i != 11 and i != 23 else (0 if i == 11 else 12)))

            if i < 12:
                connection(projected_points, i, i + 12)

        if keyboard.is_pressed('s'):
            # save image in a folder as a file
            cv2.imwrite(os.path.join('Outputs',f'{uuid.uuid1()}.jpg'),image)

        # Show frame-to-frame
        cv2.imshow("Testing",image)

        key = cv2.waitKey(10)

        if key == ord('q'):
            break
        if keyboard.is_pressed('q'):
            break

        # update pygame screen
        pygame.display.update()

    # Release and destroy all windows
    video.release()
    cv2.destroyAllWindows()