# 스위치 누르면 3.3V 신호가 GPIO로 들어감
# 스위치 안누르면 아무것도 들어가지 않음(0,1 둘다 아님) == floating 상태
# Pulldown or Pullup 저항을 달아서 누르지 않았을 떄는 GND(OV) 입력되도록 설계

from gpiozero import Button
import time

# GPIO 핀 5 버튼, 내부 풀업 저항 사용 X
SW1 = Button(5, pull_up=False)

try:
    while True:
        sw1Value = SW1.is_pressed
        print(sw1Value)
        time.sleep(0.1)

except KeyboardInterrupt:
    pass