# Generation-and-recognition-of-shapes- #

This work shows the process of generating and recognizing shapes on a two-dimensional plane. Programs written in python 3.8. The shapes are set in random order on a black background.

###  Лабораторная работа №2 по предмету "Обнаружение и Распознование сигналов" ###


| 🔢  | Ход работы   | ℹ️ |
| ------------- | ------------- |------------- |
| 1️⃣  |  Установить библиотеку opencv.  | ✅ |
| 2️⃣ | Написать скрипт генерации N картинок со случайными геометрическими фигурами случайных цветов на черном фоне (N задается с клавиатуры). Скрипт должен быть оформлен в отдельный .py файл. На каждом изображении должны быть круг,квадрат, прямоугольник, треугольник, пятиугольник. (Продвинутый вариант –добавить закругленные углы). |✅  |


Цель работы
------------
С помощью python3.8 создать программы для генерации и распознавания геометрических фигур на двумерной плоскости.


Для более хорошего понимания работы программ советую почитать [материал](https://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/)

Выполнение работы
-----------------
В файле main.py содержится программа для генерации фигур. В ней несколько функций, которые рисуют фигуры.Для каждой новой фигуры выделается место, а именно окружность таким образом чтобы новая окружность не пересекалась со всеми старыми. И потом в эту окружность вписывается новая фигура.

#### Фрагмент  когда где показана функция для вычисления евклидова расстояния между точками
```python
def dist(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
```

Результат выполнения программы:
![Генерация фигуры](https://bmstu.codes/MorozoFF/lr-2-opc/-/raw/master/1.png)

В файле shape.py содержится программа для генерации фигур. Чтобы выполнить определение формы, мы будем использовать аппроксимацию контура.Как следует из названия, аппроксимация контура - это алгоритм уменьшения количества точек на кривой с уменьшенным набором точек - отсюда и термин аппроксимация.Этот алгоритм широко известен как алгоритм Рамера-Дугласа-Пекера или просто алгоритм разделения и слияния.Аппроксимация контура основана на предположении, что кривая может быть аппроксимирована серией коротких отрезков линии. Это приводит к получению аппроксимированной кривой, которая состоит из подмножества точек, определенных исходной кривой.
Аппроксимация контура фактически уже реализована в OpenCV с помощью метода cv2.approxPolyDP. Чтобы выполнить аппроксимацию контура, мы сначала вычисляем периметр контура, а затем строим фактическую аппроксимацию контура.

#### Фрагмент кода на котором представлен метод cv2.approxPolyDP

```python
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

```

Общие значения для второго параметра cv2.approxPolyDP обычно находятся в диапазоне 1-5% от исходного периметра контура. Мы начинаем перебирать каждый из отдельных контуров. Для каждого из них мы вычисляем центр контура, а затем выполняем определение формы и маркировку.Поскольку мы обрабатываем контуры, извлеченные из изображения с измененным размером (а не из исходного изображения), нам нужно умножить контуры и центральные (x, y) -координаты на наш коэффициент изменения размера. Это даст нам правильные координаты (x, y) как для контуров, так и для центроида исходного изображения.Наконец, мы рисуем контуры и помеченную форму на нашем изображении, а затем отображаем наши результаты. Наш скрипт перебирает каждую фигуру отдельно, выполняет обнаружение формы для каждой, а затем рисует имя фигуры на объекте.
Результат выполнения программы:
![Распознование фигур](https://bmstu.codes/MorozoFF/lr-2-opc/-/raw/master/1_new.png)

Так же напоминаю для тех кому интересно выполнить задание самому или протестировать данную программу, то прошу перейти [сюда](https://drive.google.com/drive/folders/1b_molbj8z6JhHV6r178AeI1XpQezehsm?usp=sharing "Практикум по машинному обучению")
