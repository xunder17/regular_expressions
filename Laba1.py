import re
from sympy import isprime

"""Этот код вычисляет выражение, заданное пользователем, используя алгоритм Евклида для нахождения наибольшего общего делителя."""
def gcdEx(a, b):  # функция нахождения наибольшего общего делителя двух чисел
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcdEx(b % a, a)  # рекурсия
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y  # a*x+b*y=gcd(a,b)


try:
    expr = input()  # работа со строкой
    print(expr)
    expr = expr.lower()
    expr = expr.replace(" ", "")
    expr = expr.replace("mod", "%")
    expr = expr.replace("^", "**")
    expr = expr.replace("^^", "**")
    expr = expr.replace("**-1", "@")
    expr = expr.replace("**(-1)", "@")
    result = re.split('([/+*-//()%])', expr) # разделяем выражение на составляющие части
    expr = ""
    print(result)
    # вырез мод в отдельную переменную остатка деления
    mod = int(result[result.index("%") + 1])  # получаем модуль, размер поля
    result.remove(result[result.index("%") + 1])  # удаление размера поля
    result.remove("%")
    print(result)
    if isprime(mod) == False:  # проверка на простое число
        exit() # если не простое
    for i in range(len(result)):  # поиск деления деление заменяем на *
        if result[i] == '/':
            result[i] = '*'  # деление как умножение на обратный элемент
            result[i + 1] = f"{result[i + 1]}@"
    print(result)
    for i in range(len(result)): # поиск
        if result[i].find(
                "@") != -1:           # находим степень -1 и забираем его
            # a - поиск обратного эл, присываем собачку к элементам
            m, a = mod, int(result[i].replace("@", ""))
            j = i
            gcd, x, y = gcdEx(a, m)  # идем по алгоритму евклида, общий дел
            print(a, m)
            if gcd == 1:
                ans = (x % m + m) % m # обр эл
                result[j] = str(ans)  # возвращаем делитель на место
            else:
                ans = -1
    print(result)
    for i in range(len(result)):
        expr = expr + result[i]    # формируем строку
    print(expr)
    expr = f"{str(eval(expr))}%{mod}" # вычисляем выражение и добавляем модуль
    print(expr)
    print(eval(expr))
except Exception:
    print('Что-то вы сделали не так!')
