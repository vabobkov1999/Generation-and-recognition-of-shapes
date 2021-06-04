import cv2
import glob, os
import re

def recognize_shapes(filename):
    shapes = {3:'triangle', 4:'square', 5:'pentagon', 6:'hexagon'}
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #gray = cv2.GaussianBlur(gray, (5, 5), 0)
    ret, thresh = cv2.threshold(gray, 10, 255, 0)
    contours, hierarchies = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # retr_external - внешние контуры, CHAIN_APPROX_SIMPLE - сглиживание контуров
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True) #второй параметр - max рассточние аппроксимации, последнее true - замкнутый контур
        if len(approx) <=6:
            shape = shapes[len(approx)]
        else:
            shape = 'circle'

        if shape == 'square':
            x, y, w, h = cv2.boundingRect(approx) # выделение прямоугольником интересубщей области
            ar = w / float(h)
            if ar < 0.9 or ar > 1.1:
                shape = 'rectangle'
        cv2.drawContours(img, [cnt], -1, (255, 255, 255), 2) # -1 говорит что закрасить нужно все контуры
        cv2.putText(img, shape, tuple(cnt[0][0]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 1) # координаты, стиль шрифта, размер шрифта, цыет, толщина
    cv2.imwrite(f'{filename.split(".")[0]}_new.png', img)

if __name__ == '__main__':
    for file in glob.glob("*[0-9].png"):
        print(file)
        recognize_shapes(file)
