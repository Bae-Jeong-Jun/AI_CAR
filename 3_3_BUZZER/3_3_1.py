# 부저는 5V 전원과 연결됨
# 3.3V로 5V 제어 위해 NPN 트랜지스터 이용

from gpiozero import TonalBuzzer
import time

# GPIO 12핀에 연결된 부저 객체 생성
BUZZER = TonalBuzzer(12)

try:
    while True:
        # 주파수를 261Hz로 변경
        BUZZER.play(261)
        time.sleep(1.0)
        BUZZER.stop()
        time.sleep(1.0)

except KeyboardInterrupt:
    pass

BUZZER.stop()
