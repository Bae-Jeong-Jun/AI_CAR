import time
import sys
sys.path.append('/home/jj/pi/AI_CAR/5_1_CAMERA')
import mycamera
import cv2
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

camera = mycamera.MyPiCamera(640,480)

def main():
    filepath = '/home/jj/pi/AI_CAR/video/opencv/train'
    i = 0
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
            
            height, _, _ = image.shape
            image = image[int(height/2):,:,:]
            image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
            image = cv2.resize(image, (200,66))

            # 작은 노이즈(잡음)를 줄이고, 후처리를 안정적으로 만들기 위함
            image = cv2.GaussianBlur(image,(5,5),0)
            # 이진화(thresholding) 작업을 수행
            # 픽셀 값이 200 이상(밝은 영역)이면 → 0으로 (검정),픽셀 값이 200 미만(어두운 영역)이면 → 255로 (흰색)
            # 일반적인 흑백 변환이 아니라 반전된(binary inverted) 흑백 영상이 만들어짐
            _, image  = cv2.threshold(image,200,255,cv2.THRESH_BINARY_INV)    
            
            if carState == "left":
                cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 45), image)
                i += 1
            elif carState == "right":
                cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 135), image)
                i += 1
            elif carState == "go":
                cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 90), image)
                i += 1
            
            cv2.imshow('Original', image)
    
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()
    PWMA.value = 0.0
    PWMB.value = 0.0