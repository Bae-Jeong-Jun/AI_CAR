import threading
import time
import sys
sys.path.append('/home/jj/pi/AI_CAR/5_1_CAMERA')
import mycamera
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from gpiozero import DigitalOutputDevice
from gpiozero import PWMOutputDevice

PWMA = PWMOutputDevice(18)
AIN1 = DigitalOutputDevice(22)
AIN2 = DigitalOutputDevice(27)

PWMB = PWMOutputDevice(23)
BIN1 = DigitalOutputDevice(25)
BIN2 = DigitalOutputDevice(24)

def motor_go(speed):
    # 정방향
    AIN1.value = 0
    AIN2.value = 1
    PWMA.value = speed
    BIN1.value = 0
    BIN2.value = 1
    PWMB.value = speed

def motor_right(speed):
    AIN1.value = 0
    AIN2.value = 1
    PWMA.value = speed
    BIN1.value = 1
    BIN2.value = 0
    PWMB.value = 0.0

def motor_left(speed):
    AIN1.value = 1
    AIN2.value = 0
    PWMA.value = 0.0
    BIN1.value = 0
    BIN2.value = 1
    PWMB.value = speed

def motor_back(speed):
    # 역방향
    AIN1.value = 1
    AIN2.value = 0
    PWMA.value = speed
    BIN1.value = 1
    BIN2.value = 0
    PWMB.value = speed

def motor_stop():
    AIN1.value = 0
    AIN2.value = 1
    PWMA.value = 0.0
    BIN1.value = 1
    BIN2.value = 0
    PWMB.value = 0.0  

speedSet = 0.5

def img_preprocess(image):
    height, _, _ = image.shape
    image = image[int(height/2):,:,:]
    image = cv2.cvtColor(image,cv2.COLOR_BGR2YUV)
    image = cv2.GaussianBlur(image, (5,5), 0)
    image = cv2.resize(image, (200,66))
    _, image = cv2.threshold(image,200,255,cv2.THRESH_BINARY_INV)
    image = image /255
    return image

camera = mycamera.MyPiCamera(640,480)

def main():
    model_path = '/home/jj/pi/AI_CAR/model/lane_navigation_final.h5'
    model = load_model(model_path, compile=False)

    carState = 'go'

    try:
        while True:
            keyValue = cv2.waitKey(1)

            if keyValue == 0 or keyValue == 224:  # 특수키
                keyValue = cv2.waitKey(10)
            elif keyValue == 82:
                print("go")
                carState = "go"
                motor_go(speedSet)
            elif keyValue == 84:
                print("stop")
                carState = "stop"
                motor_stop()
            elif keyValue == 81:
                print("left")
                carState = "left"
                motor_left(speedSet)
            elif keyValue == 83:
                print("right")
                carState = "right"
                motor_right(speedSet)

            _, image = camera.read()
            image = cv2.flip(image, -1)
            cv2.imshow('Original', image)
            preprocessed = img_preprocess(image)
            cv2.imshow('pre', preprocessed)
            
            X = np.asarray([preprocessed])
            steering_angle = int(model.predict(X)[0])
            print("predict angle : ", steering_angle)

            if carState == "go":
                if 91 <= steering_angle <= 102:
                    print("go")
                    motor_go(speedSet)
                elif steering_angle > 103:
                    print("right")
                    motor_right(speedSet)
                elif steering_angle < 90:
                    print("left")
                    motor_left(speedSet)
            elif carState == "stop":
                motor_stop()
    
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()
    PWMA.value = 0.0
    PWMB.value = 0.0