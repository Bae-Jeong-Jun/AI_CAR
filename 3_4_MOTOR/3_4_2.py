# TB6612 모터 사용, 2개 채널 이용 

# A채널(왼쪽 모터) 속도 조절 : PWMA = GPIO 18
# A채널(왼쪽 모터) 방향 결정 : AIN1 = GPIO22, AIN2 = GPIO27 
# B채널(오른쪽 모터) 속도 조절 : PWMB = GPIO 25
# B채널(오른쪽 모터) 방향 결정 : BIN2 = GPIO24, BIN1 = GPIO23

from gpiozero import DigitalOutputDevice
from gpiozero import PWMOutputDevice
import time

PWMA = PWMOutputDevice(18)
AIN1 = DigitalOutputDevice(22)
AIN2 = DigitalOutputDevice(27)

try:
    while True:
        AIN1.value = 0
        AIN2.value = 1
        # speed : 0.0~1.0  
        # 듀티 사이클 = "신호가 켜져 있는 시간 / 전체 주기 시간" × 100%
        # 듀티 사이클이 10% 일 때, 모터가 돌지 않음
        PWMA.value = 0.1
        time.sleep(1.0)

        AIN1.value = 0
        AIN2.value = 1
        PWMA.value = 0.5
        time.sleep(1.0)

        AIN1.value = 0
        AIN2.value = 1
        PWMA.value = 1.0
        time.sleep(1.0)

        AIN1.value = 0
        AIN2.value = 1
        PWMA.value = 0.0
        time.sleep(1.0)

except KeyboardInterrupt:
    pass

PWMA.value = 0.0









