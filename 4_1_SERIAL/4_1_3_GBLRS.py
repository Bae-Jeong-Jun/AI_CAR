import serial
import time

# 시리얼 포트와 속도 설정
port = '/dev/rfcomm0'
baudrate = 9600

try:
    ser = serial.Serial(port, baudrate, timeout=1)
    print(f"Connected to {port} at {baudrate} baud.")

    while True:
        # 데이터 읽기
        received_data = ser.readline().decode()
        if received_data.find("go") >= 0:
            print("ok go")
        elif received_data.find("back") >= 0:
            print("ok back")
        elif received_data.find("left") >= 0:
            print("ok left")
        elif received_data.find("right") >= 0:
            print("ok right")
        elif received_data.find("stop") >= 0:
            print("ok stop")

except serial.SerialException as e:
    print(f"Serial error: {e}")

except KeyboardInterrupt:
    pass

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")
