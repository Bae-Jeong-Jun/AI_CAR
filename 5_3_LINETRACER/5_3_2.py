import sys
sys.path.append('/home/jj/pi/AI_CAR/5_1_CAMERA')
import mycamera
import cv2

def main():
    camera = mycamera.MyPiCamera(320,240)

    while(camera.isOpened()):
        # 카메라 프레임 값을 읽어 image에 넣음 제대로 읽으면 True 아닐시 False
        _, image = camera.read()
        image = cv2.flip(image, -1)
        cv2.imshow('normal', image)

        height, width, _ = image.shape
        # 이미지 아래부분의 1/2만 남김
        crop_img = image[height // 2 :, :]
        cv2.imshow('crop',crop_img)

        if cv2.waitKey(1) == ord('q'):
            break
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
