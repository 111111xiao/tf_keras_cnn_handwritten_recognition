import math
def calculator(l1):
    list_number = []
    list_operator = []
    list_power = [0]
    sum = j = flag = 0
    power = 1
    for i in l1:
        if i == '=':
            flag = 1
        if i != '+' and i != '-' and i != '*' and i != '/' and i != '=' and i != '^':
            sum = sum * 10 + float(i)
        elif (i == '^'):
            if (list_power[0] == 0):
                list_power[0] = sum
            else:
                list_power.insert(0,sum)
            sum = 0
        else:
            if (list_power[0] == 0):
                list_number.append(sum)
            else:
                list_power.insert(0,sum)
                for j in list_power:
                    power = j ** power
                list_number.append(power)
            sum = 0
            list_power = [0]
            power = 1
            list_operator.append(i)
    if flag == 1:
        for i in list_operator:
            if i == '*':
                list_number[j] *= list_number[j + 1]
                del list_number[j + 1]
                j -= 1
            elif i == '/':
                list_number[j] /= list_number[j + 1]
                del list_number[j + 1]
                j -= 1
            j += 1
        for i in list_operator:
            if i == '+':
                list_number[0] += list_number[1]
                del list_number[1]
            elif i == '-':
                list_number[0] -= list_number[1]
                del list_number[1]
        l1.append(str(list_number[0]))
        return l1
    else:
        l1.append('$\n\n$No Equal')
        return l1
def equation(s1,l1):
    list_number = []
    list_operator = []
    list_x = ['0']
    sum = flag = 0
    x = '+'  #x的符号位，默认为+
    for i in l1:
        if i == '=':
            flag = 1
        if flag == 0:
            if i != '+' and i != '-' and i != '*' and i != '/' and i != '=' and i != s1 and i != '^':
                sum = sum * 10 + float(i)
            elif i == s1:
                if (sum == 0):
                    sum = 1
                list_x.append(x)
                list_x.append(sum)
                sum = 0
            else:
                x = i
                list_number.append(sum)
                sum = 0
                list_number.append(i)
        elif flag == 1:
            list_number.append(sum)
            sum = 0
            list_number.append(i)
            calculator(list_number)
            flag = 2
        elif flag == 2:
            if i != '+' and i != '-' and i != '*' and i != '/' and i != '=' and i != 'x' and i != '^':
                sum = sum * 10 + float(i)
            elif i == 'x':
                if (sum == 0):
                    sum = 1
                list_x.append(x)
                list_x.append(sum)
                sum = 0
            else:
                if (i == '+'):
                    x = '-'
                elif (i == '-'):
                    x = '+'
                list_operator.append(sum)
                sum = 0
                list_operator.append(i)
    list_operator.append(sum)
    list_operator.append('=')
    calculator(list_operator)
    list_x.append('=')
    calculator(list_x)
    if (list_x[-1] == '0'):
        l1.append('$\n\n$No Equal')
        return l1
    x = (float(list_operator.pop())-float(list_number.pop())) / float(list_x.pop())
    l1.append("$\n\n$")
    l1.append(s1)
    l1.append("=")
    l1.append(str(x))
    return l1
def equation2(s1,l1):
    s_square = s1 + '^2'
    list_number = []
    list_operator = []
    list_x = ['0']
    list_x2 = ['0']
    sum = flag = 0
    x = '+'  #x的符号位，默认为+
    for i in l1:
        if i == '=':
            flag = 1
        if flag == 0:
            if i != '+' and i != '-' and i != '*' and i != '/' and i != '=' and i != s1 and i != '^' and i != s_square:
                sum = sum * 10 + float(i)
            elif i == s1:
                if (sum == 0):
                    sum = 1
                list_x.append(x)
                list_x.append(sum)
                sum = 0
            elif i == s_square:
                if (sum == 0):
                    sum = 1
                list_x2.append(x)
                list_x2.append(sum)
                sum = 0
            else:
                x = i
                list_number.append(sum)
                sum = 0
                list_number.append(i)
        elif flag == 1:
            list_number.append(sum)
            sum = 0
            list_number.append(i)
            calculator(list_number)
            flag = 2
        elif flag == 2:
            if i != '+' and i != '-' and i != '*' and i != '/' and i != '=' and i != s1 and i != '^' and i != s_square:
                sum = sum * 10 + float(i)
            elif i == s1:
                if (sum == 0):
                    sum = 1
                list_x.append(x)
                list_x.append(sum)
                sum = 0
            elif i == s_square:
                if (sum == 0):
                    sum = 1
                list_x2.append(x)
                list_x2.append(sum)
                sum = 0
            else:
                if (i == '+'):
                    x = '-'
                elif (i == '-'):
                    x = '+'
                list_operator.append(sum)
                sum = 0
                list_operator.append(i)
    list_operator.append(sum)
    list_operator.append('=')
    calculator(list_operator)
    list_x.append('=')
    calculator(list_x)
    list_x2.append('=')
    calculator(list_x2)
    if (list_x2[-1] == '0'):
        equation(l1)
        return l1
    c = (float(list_number.pop())-float(list_operator.pop()))
    b = float(list_x.pop())
    a = float(list_x2.pop())
    delta = b * b - 4 * a * c
    if (delta < 0):
        l1.append('$\n\n$Delta < 0$\nno real number$')
        return l1
    elif (delta == 0):
        x1 = (0 - b + delta ** 0.5) / 2 / a
        l1.append("$\n\n$")
        l1.append(s1)
        l1.append("1 = ")
        l1.append(s1)
        l1.append("2 = ")
        l1.append(str(x1))
        return l1
    else:
        x1 = (0 - b + delta ** 0.5) / 2 / a
        x2 = (0 - b - delta ** 0.5) / 2 / a
        l1.append("$\n\n$")
        l1.append(s1)
        l1.append("1 =  ")
        l1.append(str(x1))
        l1.append("$\n\n$")
        l1.append(s1)
        l1.append("2 =  ")
        l1.append(str(x2))
        return l1
def judge(l1):
    m = n = t = b = 0
    while (t < len(l1)):
        if l1[t] == 'x' and l1[t + 1] == '^':
            l1[t] = 'x^2'
            del(l1[t + 1])
            if (l1[t + 1] != '2'):
                l1.append('$\n\n$No Equal')
                return l1
            del(l1[t + 1])
        t += 1
    t = 0
    while (t < len(l1)):
        if l1[t] == 'y' and l1[t + 1] == '^':
            l1[t] = 'y^2'
            del(l1[t + 1])
            if (l1[t + 1] != '2'):
                l1.append('$\n\n$No Equal')
                return l1
            del(l1[t + 1])
        t += 1
    t = 0
    l = len(l1)
    l2 = {'e': math.e, '@': math.pi}
    l3 = [l2[i] if i in l2 else i for i in l1]
    l1 = l3
    for i in l1:
        if i == 'x':
            m = 1
        if i == 'y':
            m = 2
        if i == 'x^2':
            t = 1
        if i == 'y^2':
            t = 2
        if i == '=':
            n = 1
        if i == '(':
            b = 1
    if b == 1 and n == 1:
        l1.append(calculator(temp(l1)).pop())
    elif t == 1 and n == 1:
        l1 = equation2('x',l1)
    elif t == 2 and n == 1:
        l1 = equation2('y',l1)
    elif m == 1 and n == 1:
        l1 = equation('x',l1)
    elif m == 2 and n == 1:
        l1 = equation('y', l1)
    elif m == 0 and n == 1:
        l1 = calculator(l1)
    else:
        l1.append('$\n\n$No Equal')
    return l1[l:]

def temp(l1):
    m = n = t = 0
    list_number = []
    list_brackets = [0]
    for i in l1:
        if i == '(':
            m += 1
        if i == ')':
            n += 1
            t = m
        if m > 0:
            list_brackets.append(i)
        else:
            list_number.append(i)
        if m != 0 and m == n:
            list_number.append(brackets(list_brackets, t).pop())
            m = n = 0
            list_brackets = [0]
    l1 = list_number
    return l1

def brackets(l1,n):
    list = [0]
    list_temp = []
    a = 0
    while n >= 0:
        for i in l1:
            if a - 1 < n :
                list_temp.append(i)
            if i != '(' and i != ')':
                list.append(i)
            elif i == '(':
                list = [0]
                a += 1
                if a - 1 == n:
                    list_temp.pop()
            elif i == ')':
                a -= 1
                if a == n:
                    list.append('=')
                    list_temp.append(calculator(list)[-1])
                    list = [0]
        l1 = list_temp
        list_temp = []
        n -= 1
    return l1