import cv2


face_cascade_object = cv2.CascadeClassifier("Files/haarcascade_frontalface_default.xml")

img = cv2.imread("Files/photo.jpg")
# gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

face_detection = face_cascade_object.detectMultiScale(img, scaleFactor=1.05, minNeighbors=5)
# print(face_detection)
for x,y,w,h in face_detection:
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)

resized_img = cv2.resize(img,(int(img.shape[1]/2),int(img.shape[0]/2)))

cv2.imshow("Face_Detection",resized_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
