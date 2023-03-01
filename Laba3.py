import re # механизм для поиска и замены текста
import numpy as np
from numpy.polynomial import polynomial

#перевод в двоичный код
def text_bin(text,encoding="utf-8",errors = "surrogatepass"):
    bits = bin(int.from_bytes(text.encode(encoding,errors),"big"))[2:]
    return bits.zfill(8*((len(bits)+7)//8))

#Ввод данных
entry_text = input("Текст: ")
entry_text = text_bin(entry_text)
print(entry_text)

#Ввод данных
n_sum = int(input("количество сумматоров: "))
summator = []
for i in range(n_sum):
    n_reg = int(input("Количество подключенных регистров:"))
    mid_summator = []
    for j in range(n_reg):
        mid_summator.append(int(input(f"Регистр_{str(i + 1)}: ")))
        if mid_summator[j]>3:
            exit()
    summator.append(mid_summator)
print("Сумматоры:")
print(summator)

print("Закодированная последовательность:")
coded_sum = [int(entry_text[i]) for i in range(len(entry_text))]
print(coded_sum)

#переводим закодированный текст в полиномы
print("i(x):")
ix = np.poly1d(coded_sum) #polyid превращение в полином
print(ix)

#Составляем список для g(x) 
coded_sum = []
for item in summator:
    a = [0,0,0]
    for i in range(len(item)):
        a[item[i] - 1] = 1
    coded_sum.append(a)
gx =[]
for i in range(n_sum):
    gx.append(np.poly1d(coded_sum[i]))
    print(f"g{str(i + 1)}(x):")
    print(np.poly1d(coded_sum[i])) # Одномерный полиномиальный класс. 
                                   # Класс удобства, используемый для инкапсуляции “естественных” операций на многочленах так, 
                                   # чтобы упомянутые операции могли взять свою обычную форму в коде

cx = [ix * item_ for item_ in gx]
f = []
for i in range(len(cx)):
    for j in range(len(cx[i])):
        cx[i][j] = 0 if cx[i][j] % 2 == 0 else 1
    print(f"c{str(i + 1)}(x):")
    print(cx[i])

#Достаем и преобразовываем коофициенты .так же если они не равны добавляем нули в начало
    f.append(np.asarray(cx[i].coef,list).tolist()) # конвертировать входные данные в массив и преобразует массив NumPy в список Python
print("Коофициенты:")
c = 0
for item__ in f:
    c = max(c, len(item__))
print("max = ", c)
for i in range(len(f)):
    f[i] = f[i][::-1]
    print(len(f[i]))
    while len(f[i]) < c:
        f[i].append(0)
print(f)

#Делаем сравнение коофициентов
pol = []
for item___ in f:
    if len(pol) < len(item___):
        pol = item___
f.remove(pol) # удаляет первый элемент последовательности по его значению
if f:
    for item____ in f:
        for j in range(len(item____)):
            pol[j] = str(pol[j]) + str(item____[j])
print("Записываем коофициенты вместе:")
print(pol)

#Выводим закодированный текст вместе
coded_text = ""
for i in range(len(pol)):
    coded_text = coded_text + pol[i]
print("Закодированное:")
print(coded_text)

print(len(entry_text))
print(len(coded_text))

#Делаем декодирование в обратную сторону от кодирования
print("Декодирование:")
dec_pol = [coded_text[i:i+n_sum] for i in range(0, len(coded_text), n_sum)]
print(dec_pol)

dec_eq = [int(item_____[0]) for item_____ in dec_pol]
dec_eq = dec_eq[::-1]   #не забываем перевернуть тк перворачивали в декодировании
dec_eq = np.poly1d(dec_eq)
dec_eq = np.polydiv(dec_eq, gx[0]) #polydiv деление на полином
print(dec_eq[0])


f = []
strok = ""
f = np.asarray(dec_eq[0].coef,list).tolist()
for i in range(len(f)):
    f[i] = str(f[i])
    f[i] = f[i].replace(".0","")
    f[i] = f[i].replace("-", "")
    f[i] = "0" if int(f[i]) % 2 == 0 else "1"
for i in range(len(f)):
    strok = strok + str(f[i])
print(strok)

def textf(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'
print(textf(strok))