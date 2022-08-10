# 3D-Projection-Hand-Pose-Detection-Image-Video-Processing

## Description
A Python program to project 3D shapes on a 2D screen while controlling their rotation by detecting and tracking hand pose. 
I built this project because I wanted to learn and practice object detection and 3D projection. <br />
3D projection code in this project is an improvement on my final project for a course in my first-year at college. I managed to write more efficient Python code with less redundant and learned new functions to enhance my code through Leetcode practice problems and discussions. <br />
I learned Hand Pose Detection and Tracking with Mediapipe on Youtube. I learned how to control the webcam and detect objects with Python from a course called "The Python Mega Course: Build 10 Real World Applications" on Udemy.

## Features
`donutTesting.py` : main file <br />
`CapturingVideo.py` : Python code to capture video (in conjuction with Udemy course) <br />
`CircleTesting.py` : Python experimenting code to draw an ellipse with pygame <br />
`faceDetection.py` : Python code to detect human face (in conjunction with Udemy course) <br />
`handPoseDetection.py` : similar to `donutTesting.py` but without donut shape <br />
`handPoseTesting.py` : Hand pose detection and tracking code (in conjuction with a Youtube video) 

## Install and Run
Run `donutTesting.py` file.
Use python 3.9 to run Mediapipe.
In the requirements.txt, add at the end: protobuf==3.20.x. <br />
**Note:** Laptop webcam will be triggered, comment out line 469 to not show video if necessary. Show your hand in front of the camera (left or right will decide the rotation orientation of the shape). Show 2 fingers to switch from a random 3D shape to the donut shape. 


