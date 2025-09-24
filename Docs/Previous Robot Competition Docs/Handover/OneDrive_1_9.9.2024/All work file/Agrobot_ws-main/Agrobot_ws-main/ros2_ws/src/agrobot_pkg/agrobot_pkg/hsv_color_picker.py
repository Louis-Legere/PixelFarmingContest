import cv2
import numpy as np

def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        
        pixel = img[y, x]

        hsv_pixel = cv2.cvtColor(np.uint8([[pixel]]), cv2.COLOR_BGR2HSV)
        hsv_color = hsv_pixel[0][0]

        print("x: "+str(x) + "   y: "+str(y))

        print("HSV Values:", hsv_color)

# Initialize webcam
cap = cv2.VideoCapture("/dev/v4l/by-id/usb-webcamvendor_webcamproduct_00000000-video-index0")

cap.set(3, 1920)
cap.set(4, 1080)

cv2.namedWindow("Camera Feed")
cv2.setMouseCallback("Camera Feed", mouse_click)

while True:
    

    success, img = cap.read()

    if not success:
        break

    cv2.imshow("Camera Feed", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
