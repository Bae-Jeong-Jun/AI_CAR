# TB6612 모터 사용, 2개 채널 이용 

# A채널(왼쪽 모터) 속도 조절 : PWMA = GPIO 18
# A채널(왼쪽 모터) 방향 결정 : AIN1 = GPIO22, AIN2 = GPIO27 
# B채널(오른쪽 모터) 속도 조절 : PWMB = GPIO 23
# B채널(오른쪽 모터) 방향 결정 : BIN2 = GPIO24, BIN1 = GPIO25
import threading
import serial
import time
from gpiozero import DigitalOutputDevice, PWMOutputDevice

# 시리얼 설정
port = '/dev/rfcomm0'
baudrate = 9600

# 스레드 종료 신호
stop_event = threading.Event()

# 두 개 이상의 스레드가 전역변수 사용시 Race Condition(경쟁 상태) 발생 가능
# lock을 통해 방지
lock = threading.Lock() 

gData = ""

# TB6612 핀 설정
PWMA = PWMOutputDevice(18)
AIN1 = DigitalOutputDevice(22)
AIN2 = DigitalOutputDevice(27)

PWMB = PWMOutputDevice(23)
BIN1 = DigitalOutputDevice(25)
BIN2 = DigitalOutputDevice(24)

# 모터 함수들
def motor_go(speed):
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
    AIN1.value = 1
    AIN2.value = 0
    PWMA.value = speed
    BIN1.value = 1
    BIN2.value = 0
    PWMB.value = speed

def motor_stop():
    AIN1.value = 0
    AIN2.value = 0
    PWMA.value = 0
    BIN1.value = 0
    BIN2.value = 0
    PWMB.value = 0

# 시리얼 수신 스레드
def serial_thread(ser, stop_event):
    global gData
    while not stop_event.is_set():
        if ser.in_waiting > 0:
            try:
                received_data = ser.readline().decode(errors='ignore').strip()
                with lock: # lock 획득한 스레드만 해당 자원 접근
                    gData = received_data
            except Exception as e:
                print("Decode error:", e)
        else:
            time.sleep(0.1)

# 메인 함수: 명령어에 따른 모터 제어
def main():
    global gData
    speed = 0.3  # 안전하게 낮은 속도부터 시작
    while not stop_event.is_set():
        with lock:
            data = gData
            gData = ""
        if data:
            print("Received command:", data)
            if "go" in data:
                print('ok go')
                motor_go(speed)
            elif "right" in data:
                print('ok right')
                motor_right(speed)
            elif "left" in data:
                print('ok left')
                motor_left(speed)
            elif "back" in data:
                print('ok back')
                motor_back(speed)
            elif "stop" in data:
                print('ok stop')
                motor_stop()
        time.sleep(0.1)

try:
    ser = serial.Serial(port, baudrate, timeout=1)
    print(f"Connected to {port} at {baudrate} baud.")

    t = threading.Thread(target=serial_thread, args=(ser, stop_event))
    t.start()

    main()

except serial.SerialException as e:
    print(f"Serial error: {e}")

except KeyboardInterrupt:
    print("KeyboardInterrupt received. Exiting...")

finally:
    stop_event.set()
    t.join()
    if 'ser' in locals() and ser.is_open:
        ser.close()
    motor_stop()
    print("Serial port closed. Motors stopped.")
