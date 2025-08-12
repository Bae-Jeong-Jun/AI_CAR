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

        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        # 중심에 있는 픽셀에 높은 가중치 부여하는 블러링
        blur = cv2.GaussianBlur(gray,(5,5),0)

        # 임계점 처리. 픽셀 밝기가 190보다 큰 값을 255로 변환 190보다 작으면 0
        # THRESH_BINARY_INV는 흑백 표현 위함
        ret, thresh1 = cv2.threshold(blur,190,255,cv2.THRESH_BINARY_INV)

        # 이미지 압축, 팽창하여 노이즈 없앰
        mask = cv2.erode(thresh1, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cv2.imshow('mask',mask)

        # 이미지 윤곽선 검출
        contours,hierarchy = cv2.findContours(mask.copy(),1,cv2.CHAIN_APPROX_NONE)

        if len(contours) > 0:
            # 윤곽선의 최댓갑 반환
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)

            # x,y 축의 무게중심
            # 선이 중심보다 왼쪽 : 무게중심 190~250
            # 선이 중심보다 오른쪽 : 무게중심 80~130
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            print(cx)

        if cv2.waitKey(1) == ord('q'):
            break
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()