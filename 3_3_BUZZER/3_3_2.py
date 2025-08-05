from gpiozero import TonalBuzzer
import time

# GPIO 12핀에 연결된 부저 객체 생성
BUZZER = TonalBuzzer(12)

try:
    while True:
        BUZZER.play(261)
        time.sleep(1.0)
        BUZZER.play(293)
        time.sleep(1.0)
        BUZZER.play(329)
        time.sleep(1.0)
        BUZZER.play(349)
        time.sleep(1.0)
        BUZZER.play(391)
        time.sleep(1.0)
        BUZZER.play(440)
        time.sleep(1.0)
        BUZZER.play(493)
        time.sleep(1.0)
        BUZZER.play(523)
        time.sleep(1.0)
        BUZZER.stop()
        time.sleep(1.0)

except KeyboardInterrupt:
    pass

BUZZER.stop()
