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
    PWMB.value = speed

def motor_left(speed):
    AIN1.value = 1
    AIN2.value = 0
    PWMA.value = speed
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
    BIN1.value = 0
    BIN2.value = 1
    PWMB.value = 0.0  

def main():
    camera = mycamera.MyPiCamera(320,240)

    while(camera.isOpened()):
        # 카메라 프레임 값을 읽어 image에 넣음 제대로 읽으면 True 아닐시 False
        _, image = camera.read()
        image = cv2.flip(image, -1)
        cv2.imshow('normal', image)

        height, width, _ = image.shape
        # 이미지 아래부분의 1/2만 남김
        crop_img = image[height // 2 :, :]

        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        # 중심에 있는 픽셀에 높은 가중치 부여하는 블러링
        blur = cv2.GaussianBlur(gray,(5,5),0)

        # 임계점 처리. 픽셀 밝기가 190보다 큰 값을 255로 변환 190보다 작으면 0
        # THRESH_BINARY_INV는 흑백 표현 위함
        ret, thresh1 = cv2.threshold(blur,190,255,cv2.THRESH_BINARY_INV)

        # 이미지 압축, 팽창하여 노이즈 없앰
        mask = cv2.erode(thresh1, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cv2.imshow('mask',mask)

        # 이미지 윤곽선 검출
        contours,hierarchy = cv2.findContours(mask.copy(),1,cv2.CHAIN_APPROX_NONE)

        if len(contours) > 0:
            # 윤곽선 중 픽셀이 가장 많은 윤곽선 반환
            c = max(contours, key=cv2.contourArea)

            M = cv2.moments(c) # 윤곽선의 기하학적 모멘트 반환
            # m00: 윤곽선 내부의 전체 픽셀 개수
            # m10: 윤곽선 내부의 모든 픽셀의 x좌표 합
            # m01: 윤곽선 내부의 모든 픽셀의 y좌표 합
            # cx,cy는 x,y 축의 무게중심
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            
            # 픽셀 width 범위
            # 선이 중심보다 왼쪽 : 무게중심 190~240
            # 선이 중심보다 오른쪽 : 무게중심 80~157
            if 190 <= cx <= 240:
                print(cx,"Turn Left!")
                motor_left(0.3)
            elif 80 <= cx <= 157:
                print(cx,"Turn Right!")
                motor_right(0.3)
            else:
                print(cx,"Go")
                motor_go(0.3)

        if cv2.waitKey(1) == ord('q'):
            break
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
    PWMA.value = 0.0
    PWMB.value = 0.0