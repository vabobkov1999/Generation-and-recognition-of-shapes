import cv2
import math
import numpy as np
import random as ran

occupied = [[(0, 0), 0]] # массив хранит центры и радиусы всех окружностей


def dist(point1, point2): #функция для евклидова расстояния между точками
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def rotate(points, number, center): #поворачиваем точки фигуры вокруг центра фигуры
    new_points = points
    angle = get_angle(number)
    for point in new_points:
        point[0] -= center[0]
        point[1] -= center[1]
        x_new = point[0] * math.cos(angle) - point[1] * math.sin(angle)
        y_new = point[0] * math.sin(angle) + point[1] * math.cos(angle)
        point[0] = x_new + center[0]
        point[1] = y_new + center[1]
    return new_points


def draw(image, points, colour): # закрашиваем фигуру по её точкам
    pts = np.asarray(points, dtype=np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.fillPoly(image, [pts], colour)
    return True


def good_point(centre, radius): #проверяем пересечется ли новая окружность со всеми остальными
    for point in occupied:
        if dist(centre, point[0]) < (radius + point[1] + 30):
            return False
    return True


def get_coordinates(mode, centre=[0, 0], radius=0): #либо получаем координаты центра окружности либо 3 точки треугольника
    if mode == 1:
        return [ran.randint(250, 750), ran.randint(250, 750)]
    elif mode == 3:
        if centre[0] < 200 or centre[1] < 200 or centre[0] > 800 or centre[1] > 800:
            return False
        coordinates = []
        for i in range(3):
            coordinates.append(get_coordinates(1))
            while dist(coordinates[i], centre) > radius or dist(coordinates[i], centre) < (0.9 * radius):
                coordinates[i] = get_coordinates(1)
        return coordinates


def get_sides(mode): # получаем случайные стороны и углы поворота фигуры строки 54-73
    if mode == 1:
        return ran.randint(50, 100)
    elif mode == 2:
        return ran.randint(100, 150), ran.randint(100, 150)
    elif mode == 3:
        return ran.randint(100, 150), ran.randint(100, 150), ran.randint(100, 150)
    else:
        return None


def get_colour():
    colour = []
    for i in range(3):
        colour.append(ran.randint(50, 255))
    return colour


def get_angle(number):
    return ran.randint(0, 3142) / number / 1000


def draw_circle(image, center, radius, colour): #рисуем круг
    cv2.circle(image, tuple(center), radius, colour, -1)
    return True


def draw_triangle(image, center, radius, colour): # подбираем точки труегольника так чтоб расстояние между ними не было совсем малым
    points = get_coordinates(3, center, radius)
    dist0_1 = dist(points[0], points[1])
    dist0_2 = dist(points[0], points[2])
    dist1_2 = dist(points[1], points[2])
    while dist0_1 < 40 or dist0_2 < 40 or dist1_2 < 40:
        points = get_coordinates(3, center, radius)
        dist0_1 = dist(points[0], points[1])
        dist0_2 = dist(points[0], points[2])
        dist1_2 = dist(points[1], points[2])
    points = rotate(points, 3, center)
    draw(image, points, colour)
    return True


def draw_rectangle(image, center, radius, colour): #рисуем прямоугольник
    angle = get_angle(4)
    side_a = get_sides(1)
    side_b = int(math.sqrt((2 * radius) ** 2 - side_a ** 2))

    point1 = [center[0] - side_a // 2, center[1] - side_b // 2]
    point2 = [center[0] - side_a // 2, center[1] + side_b // 2]
    point3 = [center[0] + side_a // 2, center[1] + side_b // 2]
    point4 = [center[0] + side_a // 2, center[1] - side_b // 2]
    points = [point1, point2, point3, point4]
    points = rotate(points, 4, center)
    draw(image, points, colour)
    return None


def draw_pentagon(image, center, radius, colour): #рисуем 5ти
    point1 = [center[0], center[1] + radius]
    point2 = [int(center[0] + radius * math.cos(0.314)), int(center[1] + radius * math.sin(0.314))]
    point3 = [int(center[0] + radius * math.cos(0.942)), int(center[1] - radius * math.sin(0.942))]
    point4 = [int(center[0] - radius * math.cos(0.942)), int(center[1] - radius * math.sin(0.942))]
    point5 = [int(center[0] - radius * math.cos(0.314)), int(center[1] + radius * math.sin(0.314))]
    points = [point1, point2, point3, point4, point5]
    points = rotate(points, 5, center)
    draw(image, points, colour)
    return None


def draw_hexagon(image, center, radius, colour): #рисуем  и 6ти уголник
    point1 = [center[0] + radius, center[1]]
    point2 = [int(center[0] + radius * math.cos(1.047)), int(center[1] + radius * math.sin(1.047))]
    point3 = [int(center[0] - radius * math.cos(1.047)), int(center[1] + radius * math.sin(1.047))]
    point4 = [center[0] - radius, center[1]]
    point5 = [int(center[0] - radius * math.cos(1.047)), int(center[1] - radius * math.sin(1.047))]
    point6 = [int(center[0] + radius * math.cos(1.047)), int(center[1] - radius * math.sin(1.047))]
    points = [point1, point2, point3, point4, point5, point6]
    points = rotate(points, 6, center)
    draw(image, points, colour)

    return None


def draw_figure(image, num_sides): # в зависимости от числа сторон понимаем какую фигуру надо римовать
    center = get_coordinates(1)
    radius = get_sides(1)
    k = 0
    while good_point(center, radius) == False:
        center = get_coordinates(1)
        k += 1
        if k == 500:
            return False
    occupied.append([center, radius])
    colour = get_colour()
    if num_sides == 0:
        return draw_circle(image, center, radius, colour)
    elif num_sides == 3:
        return draw_triangle(image, center, radius, colour)
    elif num_sides == 4:
        return draw_rectangle(image, center, radius, colour)
    elif num_sides == 5:
        return draw_pentagon(image, center, radius, colour)
    elif num_sides == 6:
        return draw_hexagon(image, center, radius, colour)
    else:
        return False
    return False


img = np.zeros((1000, 1000, 3), dtype="uint8")
# создаем поле для рисования и формируем число сторон фигуры
for i in range(10):
    number = 1
    while number == 1 or number == 2:
        number = ran.randint(0, 6)
    draw_figure(img, number)




cv2.imshow('dark', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('1.png', img)
