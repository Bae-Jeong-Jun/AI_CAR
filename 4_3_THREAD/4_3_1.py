import threading
import serial
import time

port = '/dev/rfcomm0'
baudrate = 9600

# 이 신호가 set() 되면, 스레드들이 반복문을 멈추고 종료
stop_event = threading.Event()
gData = ""

def serial_thread(ser, stop_event):
    global gData
    while not stop_event.is_set():
        if ser.in_waiting > 0:
            try:
                received_data = ser.readline().decode(errors='ignore').strip()
                gData = received_data
            except Exception as e:
                print("Decode error:", e)
        else:
            time.sleep(0.1)  # CPU 과부하 방지

# main 함수로 gData 갖고오기
def main():
    global gData
    while not stop_event.is_set():
        print("serial dadta : ", gData)
        time.sleep(1.0)

try:
    ser = serial.Serial(port, baudrate, timeout=1)
    print(f"Connected to {port} at {baudrate} baud.")

    # Thread 이용하여 통신기능 분리
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
        print("Serial port closed.")
