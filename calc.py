# СДЕЛАНО: База, 1, 3, 4, 5
TO_NUMBER = {"один": 1, "одна": 1, "два": 2, "две": 2, "три": 3, "четыре": 4, "пять": 5, "шесть": 6, "семь": 7, "восемь": 8, "девять": 9, "ноль": 0,\
    "одиннадцать": 11, "двенадцать": 12, "тринадцать": 13, "четырнадцать": 14, "пятнадцать": 15, "шестнадцать": 16, "семнадцать": 17, \
    "восемнадцать": 18, "девятнадцать": 19, "десять": 10, "двадцать": 20, "тридцать": 30, "сорок": 40, "пятьдесят": 50, \
    "шестьдесят": 60, "семьдесят": 70, "восемьдесят": 80, "девяносто": 90, "сто": 100, "двести": 200, "триста": 300, "четыреста": 400, \
    "пятьсот": 500, "шестьсот": 600, "семьсот": 700, "восемьсот": 800, "девятьсот": 900, "одна тысяча": 1000, "две тысячи": 2000, \
    "три тысячи" : 3000, "четыре тысячи": 4000, "пять тысяч": 5000, "шесть тысяч": 6000, "семь тысяч": 7000, \
    "восемь тысяч": 8000, "девять тысяч": 9000, "десять тысяч": 10000}
TO_STRING = {0: 'ноль', 1: 'одна', 2: 'две', 3: 'три', 4: 'четыре', 5: 'пять', 6: 'шесть', 7: 'семь', 8: 'восемь', 9: 'девять', \
    10: 'десять',11: 'одиннадцать', 12: 'двенадцать', 13: 'тринадцать', 14: 'четырнадцать', 15: 'пятнадцать', 16: 'шестнадцать', \
    17: 'семнадцать',18: 'восемнадцать', 19: 'девятнадцать', 20: 'двадцать', 30: 'тридцать', 40: 'сорок', 50: 'пятьдесят', \
    60: 'шестьдесят', 70: 'семьдесят', 80: 'восемьдесят', 90: 'девяносто', 100: 'сто', 200: 'двести', 300: 'триста', \
    400: 'четыреста', 500: 'пятьсот', 600: 'шестьсот', 700: 'семьсот', 800: 'восемьсот', 900: 'девятьсот', 1000: 'одна тысяча', \
    2000: 'две тысячи', 3000: 'три тысячи', 4000: 'четыре тысячи', 5000: 'пять тысяч', 6000: 'шесть тысяч', 7000: 'семь тысяч', \
    8000: 'восемь тысяч', 9000: 'девять тысяч', 10000: 'десять тысяч'}
FLOAT_DICT = {"десят": 10, "сот": 100, "тысячн": 1000, "десятитысячн": 10000, "статысячн": 100000, "миллионн": 1000000}
FLOAT_BEGINS = {1: "десят", 2: "сот", 3: "тысячн", 4: "десятитысячн", 5: "статысячн", 6: "миллионн"}
OPERATIONS = {"плюс": "+", "минус": "-", "умножить на": "*", "разделить на": "/", "скобка открывается": "(", "скобка закрывается": ")", "в степени": "**"}
FLOAT_ENDINGS = {"ых": lambda x: x % 10 != 1 or x == 11, "ое": lambda x: x % 10 == 1 and x != 1 and x != 11, "ая": lambda x: x == 1}
def check_period(number):
    ln = len(number)
    for i in range(1, ln):
        period = (number[:i] * ln)[:ln]
        if period == number:
            return number[:i]
    return False
def print_result(number):
    if number in TO_STRING.keys(): return TO_STRING[number]
    def int_help(number):
        result = [] if number >= 0 else ["минус"]
        number = abs(number)
        for x in reversed(list(TO_STRING)):
            if number - x >= 0:
                result.append(TO_STRING[x])
                number -= x
            if number == 0:
                break
        return result
    if isinstance(number, int):
        return " ".join(int_help(number))
    else:
        integer_part, float_part = str(number).split(".")
        result = int_help(int(integer_part)) + ["и"] + int_help(int(float_part))
        ending = FLOAT_BEGINS[len(float_part)]
        for x in FLOAT_ENDINGS:
            if FLOAT_ENDINGS[x](int(float_part)):
                ending += x
                break
        result += [ending]
    if integer_part == "0":
        result = ["ноль"] + result
    return " ".join(result)
def fix_float(string):
    flag = False
    stack = []
    result = []
    for i in range(len(string)):
        if string[i] == "и":
            flag = True
        elif any([str(string[i]).endswith(k) for k in FLOAT_ENDINGS]):
            flag = False
            temp = None
            for k in FLOAT_DICT:
                if string[i].startswith(k):
                    break
            if sum(stack) == 0:
                temp = result.pop()
                while temp not in OPERATIONS.values():
                    stack.append(temp)
                    if len(result) == 0:
                        break
                    temp = result.pop()
            result.append(temp) if temp in OPERATIONS.values() else None
            float_result = sum(stack) / FLOAT_DICT[k]
            result.append(float_result) if check_period(float_result) else result.append(round(float_result, 6))
            stack = []
        if flag and string[i] != "и":
            stack.append(string[i])
        elif (not flag) and string[i] != "и" and (not any([str(string[i]).endswith(k) for k in FLOAT_ENDINGS])):
            result.append(string[i])
    return result
def calc():
    string = input("Введите арифметическое выражение словами: ")
    for k in OPERATIONS: #операции
        if k in string:
            string = string.replace(k, OPERATIONS[k])
    string = string.split()
    for i in range(len(string)): #целые числа
        if string[i] in TO_NUMBER:
            string[i] = TO_NUMBER[string[i]]
    string = fix_float(string)
    numbers = []
    sm = 0
    for i in range(len(string)):
        var = "операция" if string[i] in OPERATIONS.values() else "число"
        if var == "число":
            sm += string[i]
        else:
            if sm != 0: numbers.append(str(sm))
            numbers.append(string[i])
            sm = 0
    numbers.append(str(sm))
    result_int = eval(" ".join(numbers))
    result_string = print_result(result_int)
    print(result_string)
calc()