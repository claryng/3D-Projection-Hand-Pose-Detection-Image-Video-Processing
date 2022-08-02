import cv2

# Create an object to read video
video = cv2.VideoCapture(0)

# Create the first frame (static frame)
first_frame = None

while True:
    # Capture the frame
    check, frame = video.read()

    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    # Blur the image
    blurred_frame = cv2.GaussianBlur(gray_frame,(21,21),5)

    # Assign first_frame to the static frame to compare with next frames
    if first_frame is None:
        first_frame = gray_frame
        continue

    # Delta frame
    delta_frame = cv2.absdiff(first_frame,blurred_frame)

    # Threshold frame
    threshold_frame = cv2.threshold(delta_frame,50,255,cv2.THRESH_BINARY)[1]

    # Dilate image
    threshold_frame = cv2.dilate(threshold_frame, None, iterations=2)

    # Find contours in the copied frame so that the original one
    # is not modified
    (cnts,_) = cv2.findContours(threshold_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # Draw green rects for detected moving objects
    for contour in cnts:
        # Check the contour area
        # if it is less then 1000 pixels, it is not moving objects
        if cv2.contourArea(contour) < 1000:
            continue

        # Otherwise, draw a rectangle around the moving object

        # First, get the coordinates of the area of the contour
        (x,y,w,h) = cv2.boundingRect(contour)

        # Second, draw the rectangle
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)

    # Show frame-to-frame
    cv2.imshow("Captured",frame)

    # wait for 100 milliseconds before showing the next frame
    key = cv2.waitKey(100)

    # Stop video when pressing 'q'
    if key == ord('q'):
        break

# Release and destroy the video
video.release()
cv2.destroyAllWindows()