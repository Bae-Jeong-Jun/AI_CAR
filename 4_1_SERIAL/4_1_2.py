# GPIO 15(TXD), 14(RXD)번 핀이 시리얼 통신용으로 할당됨
# 라즈베리파이의 우분투OS는 블루투스 설정이 자 안됨
import serial
import time

bleSerial = serial.Serial("/dev/ttyAMA10", baudrate=9600, timeout=1.0)

try:
    while True:
        sendData = "i am rasberry \r\n"
        bleSerial.write(sendData.encode())
        time.sleep(1.0)
        
except KeyboardInterrupt:
    pass

bleSerial.close()

