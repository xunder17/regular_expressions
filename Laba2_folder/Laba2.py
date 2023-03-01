from random import randint #помехоустойчивое кодирование
from PIL import Image, ImageDraw

Debug = 2 #вид вывода результата

image = Image.open('picture.jpg')  
image2 = image.copy() 
draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования
width, height = image.size # Определяем ширину и высоту
pix = image.load()  # Выгружаем значения пикселей

image.save("task1.jpg", "JPEG") 

# 2 пункт: значение пикселя переводим в бинарный вид, в каждое значение
def binary(value):      
    # вносим ошибки (количество ошибок всегда = 1), возвращаем десятичный вид и выводим
    pos = 1 << randint(0, 7) # случайный бит(сдвигаем биты числа влево на заданное кол-во позиций) 
    return value ^ pos # сложение по модулю 2
    # вносим ошибки (количество ошибок от 1 до t), возвращаем десятичный вид и выводим


# 3 пункт: тоже самое, что и во втором пункте, но с кодированием кодом Хэмминга
pix = image2.load()  # Выгружаем значения пикселей, двоичные числа в картинку

# допустим 'C' - контрольные биты, 'b' - оригинальные биты слова
# CCbCbbbCbbbb -> 0, 1, 3, 7 - контрольные биты
# теперь укажем через 'C' - где находится контрольный бит, 'x' - какие биты суммируем, '_' - а какие не суммируем
# C_x_x_x_x_x_ -> 0, 1, 3, 4 и 6 - биты для первого контрольного бита
#_Cx__xx__xx_ -> 0, 2, 3, 5 и 6 - биты для второго контрольного бита
#___Cxxx____x -> 1, 2, 3 и 7 - биты для третьего контрольного бита
#_______Cxxxx -> 4, 5, 6 и 7 - биты для четвёртого контрольного бита
#Контрольный бит удлиняет слово и добавляет информацию, чтобы защитить от ошибок

def encoder(orig):      # функция находит контрольные биты в слове и собирает результат из 12 битов, где 4 из них - контрольные
    ctrl_bit1 = str((int(orig[0]) + int(orig[1]) + int(orig[3]) + int(orig[4]) + int(orig[6])) % 2)
    ctrl_bit2 = str((int(orig[0]) + int(orig[2]) + int(orig[3]) + int(orig[5]) + int(orig[6])) % 2)
    ctrl_bit3 = str((int(orig[1]) + int(orig[2]) + int(orig[3]) + int(orig[7])) % 2)
    ctrl_bit4 = str((int(orig[4]) + int(orig[5]) + int(orig[6]) + int(orig[7])) % 2)
    return (
        ctrl_bit1
        + ctrl_bit2
        + orig[0]
        + ctrl_bit3
        + orig[1]
        + orig[2]
        + orig[3]
        + ctrl_bit4
        + orig[4:]
    )

def decoder(result):      # функция декодирования, которая пытается восстановить испорченные биты (буквы с ошибками)
    error_str = result[2] + result[4] + result[5] + result[6] + result[8:] #вычленяем из входных данных только биты слова
    check_str = encoder(error_str)
    a = (result[0] != check_str[0]) # проверяем первый контрольный бит 
    b = (result[1] != check_str[1]) << 1 # проверяем второй контрольный бит
    c = (result[3] != check_str[3]) << 2 # проверяем третий контрольный бит
    d = (result[7] != check_str[7]) << 3 # проверяем четвёртый контрольный бит
    pos = a + b + c + d - 1 #0 или ошибка
    # позиция испорченного бита ни с проста нумеруется от 1,
    # чтобы (a + b + c + d - 1) могло выдавать -1, если ошибок нет
    if pos < 12 and pos != -1:
        recovered_str = result[:pos] + str(1 - int(result[pos])) + result[pos + 1:] # пытаемся исправить ошибку заменой 0 на 1 в определенной позиции
    else:
        recovered_str = result # если ошибок нет (pos == -1) или повреждено больше одной буквы (pos >= 12), то восстановление не применяется
    new_pix = recovered_str[2] + recovered_str[4] + recovered_str[5] + recovered_str[6] + recovered_str[8:]
    return check_str, recovered_str, new_pix # то, что выводится в консоли

"""Main function of generation scares and return the new picture"""
def binary2(value):      # функция переводит в двоичную систему, кодирует, добавляет ошибки и декодирует
    orig = bin(value)[2:] # оригинальное слово
    orig = orig.rjust(8, "0") # дописываем незначащие нули в начало так, чтобы в итоге длина слова всегда была равна 8
    error_str = bin(binary(value))[2:] # испорченное слово
    error_str = error_str.rjust(8, "0") # дописываем незначащие нули в начало так, чтобы в итоге длина слова всегда была равна 8
    def_str = encoder(orig) # защищённое оригинальное слово
    result = def_str[0] + def_str[1] + error_str[0] + def_str[3] + error_str[1] + error_str[2] + error_str[3] + def_str[7] + error_str[4:] # подменяем биты на испорченные
    check_str, recovered_str, new_pix = decoder(result)
    if Debug == 1: print(orig, "->", result, "->", new_pix)
    elif Debug > 1: print(orig, "->", def_str, "->", result, "->", check_str, "->", recovered_str, "->", new_pix) 
    return int(new_pix, 2)
    
for y in range(height):
    for x in range(width):
        r, g, b = map(binary, pix[x, y]) # каждый цветовой канал прогоняем отдельно
        
        draw.point((x, y), (r, g, b)) #рисуем пиксель

image.save("task2.jpg", "JPEG") 

for y in range(height):
    for x in range(width):
        r, g, b = map(binary2, pix[x, y]) # каждый цветовой канал прогоняем отдельно
        draw.point((x, y), (r, g, b)) #рисуем пиксель

image.save("task3.jpg", "JPEG") #не забываем сохранить изображение