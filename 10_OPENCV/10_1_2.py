import time
import sys
sys.path.append('/home/jj/pi/AI_CAR/5_1_CAMERA')
import mycamera
import cv2

camera = mycamera.MyPiCamera(640,480)

def main():
    try:
        while True:
            keyValue = cv2.waitKey(1)

            if keyValue == ord('q'):
                break

            _, image = camera.read()
            image = cv2.flip(image, -1)
            cv2.imshow('Original', image)
            
            height, _, _ = image.shape
            image = image[int(height/2):,:,:]
            image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
            image = cv2.resize(image, (200,66))

            # 작은 노이즈(잡음)를 줄이고, 후처리를 안정적으로 만들기 위함
            image = cv2.GaussianBlur(image,(5,5),0)
            # 이진화(thresholding) 작업을 수행
            # 픽셀 값이 200 이상(밝은 영역)이면 → 0으로 (검정),픽셀 값이 200 미만(어두운 영역)이면 → 255로 (흰색)
            # 일반적인 흑백 변환이 아니라 반전된(binary inverted) 흑백 영상이 만들어짐
            _, image  = cv2.threshold(image,200,255,cv2.THRESH_BINARY_INV)    
            cv2.imshow('processed', image)
    
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()