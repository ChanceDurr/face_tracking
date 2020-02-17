import cv2
import pigpio

pi = pigpio.pi(host='192.168.1.32')

cam_min = 550
cam_mid = 1425
cam_max = 2300

# Set camera to middle position
pi.set_servo_pulsewidth(12, cam_mid)
cam_position = cam_mid

cascPath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    width = int(video_capture.get(3))
    height = int(video_capture.get(4))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=8,
        minSize=(100, 100),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    face_x = None

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        face_x = x

    # Create a boundary of where we want the face
    cv2.rectangle(frame, (850, 0), (width-850, height), (255, 0, 0), 2)

    # If face not in boundary, move camera to desired position
    if face_x != None:
        # move to left
        if face_x < 850:
            if cam_position > 550:
                cam_position += 9
                pi.set_servo_pulsewidth(12, cam_position)

        # move to right
        if face_x > width-850:
            if cam_position < 2300:
                cam_position -= 9
                pi.set_servo_pulsewidth(12, cam_position)
        


    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()