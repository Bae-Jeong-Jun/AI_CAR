import sys
sys.path.append('/home/jj/pi/AI_CAR/5_1_CAMERA')
import mycamera
import cv2

def main():
    camera = mycamera.MyPiCamera(640,480)

    while(camera.isOpened()):
        # 카메라 프레임 값을 읽어 image에 넣음 제대로 읽으면 True 아닐시 False
        _, image = camera.read()
        cv2.imshow('camera test', image)

        if cv2.waitKey(1) == ord('q'):
            break
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
