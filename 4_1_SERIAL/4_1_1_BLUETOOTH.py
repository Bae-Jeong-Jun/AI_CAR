# GPIO 15(TXD), 14(RXD)번 핀이 시리얼 통신용으로 할당됨
import serial

bleSerial = serial.Serial("/dev/ttyAMA10", baudrate=9600, timeout=1.0)

try:
    while True:
        line = bleSerial.readline()  # CR+LF 기준 한 줄 읽기
        print(line.decode('utf-8').strip())  # 바이트->문자열 변환 후 양쪽 공백 제거

except KeyboardInterrupt:
    pass

bleSerial.close()
