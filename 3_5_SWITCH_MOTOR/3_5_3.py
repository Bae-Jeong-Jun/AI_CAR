# TB6612 모터 사용, 2개 채널 이용 

# A채널(왼쪽 모터) 속도 조절 : PWMA = GPIO 18
# A채널(왼쪽 모터) 방향 결정 : AIN1 = GPIO22, AIN2 = GPIO27 
# B채널(오른쪽 모터) 속도 조절 : PWMB = GPIO 25
# B채널(오른쪽 모터) 방향 결정 : BIN2 = GPIO24, BIN1 = GPIO23

from gpiozero import Button
from gpiozero import DigitalOutputDevice
from gpiozero import PWMOutputDevice
import time

SW1 = Button(5, pull_up=False)
SW2 = Button(6, pull_up=False)
SW3 = Button(13, pull_up=False)
SW4 = Button(19, pull_up=False)

PWMA = PWMOutputDevice(18)
AIN1 = DigitalOutputDevice(22)
AIN2 = DigitalOutputDevice(27)

PWMB = PWMOutputDevice(23)
BIN1 = DigitalOutputDevice(25)
BIN2 = DigitalOutputDevice(24)

try:
    while True:
        if SW1.is_pressed == True:
            print("go")
            # 정방향
            AIN1.value = 0
            AIN2.value = 1
            PWMA.value = 0.5
            BIN1.value = 0
            BIN2.value = 1
            PWMB.value = 0.5
        elif SW2.is_pressed == True:
            print("right")
            AIN1.value = 0
            AIN2.value = 1
            PWMA.value = 0.5
            BIN1.value = 1
            BIN2.value = 0
            PWMB.value = 0.5
        elif SW3.is_pressed == True:
            print("left")
            AIN1.value = 1
            AIN2.value = 0
            PWMA.value = 0.5
            BIN1.value = 0
            BIN2.value = 1
            PWMB.value = 0.5
        elif SW4.is_pressed == True:
            print("back")
            # 역방향
            AIN1.value = 1
            AIN2.value = 0
            PWMA.value = 0.5
            BIN1.value = 1
            BIN2.value = 0
            PWMB.value = 0.5
        else:
            print("stop")
            AIN1.value = 0
            AIN2.value = 1
            PWMA.value = 0.0
            BIN1.value = 0
            BIN2.value = 1
            PWMB.value = 0.0
        
        time.sleep(1.0)

except KeyboardInterrupt:
    pass

PWMA.value = 0.0
PWMB.value = 0.0