import serial
import time

# 시리얼 포트와 속도 설정
port = '/dev/rfcomm0'
baudrate = 9600

try:
    ser = serial.Serial(port, baudrate, timeout=1)
    print(f"Connected to {port} at {baudrate} baud.")

    while True:
        # 데이터 보내기
        send_data = "Hello from Raspberry Pi!\r\n"
        ser.write(send_data.encode())
        print(f"Sent: {send_data.strip()}")

        # 데이터 읽기
        if ser.in_waiting > 0:
            received_data = ser.readline().decode().strip()
            print(f"Received: {received_data}")

        time.sleep(1)

except serial.SerialException as e:
    print(f"Serial error: {e}")

except KeyboardInterrupt:
    print("Program interrupted by user.")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")
