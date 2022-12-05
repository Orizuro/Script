def make_table(variables):
    n = len(variables)
    w = n + 1
    h = 2**n + 1
    interval = 2**n
    fill = 0
    matrix = [[0 for x in range(w)] for y in range(h)]
    for j in range(0, n):
        matrix[0][j] = variables[j]
        interval = int(interval / 2)
        counter = 1
        for i in range(1, h):
            matrix[i][j] = fill
            if counter == interval:
                counter = 0
                if fill == 0:
                    fill = 1
                else:
                    fill = 0
            counter += 1
    return matrix


def logic_operator(c, a, b):
    if c == "/":
        if a == 1 and b == 1:
            return 0
        else:
            return 1
    if c == "*":
        if a == 1 and b == 1:
            return 1
        else:
            return 0
    if c == "+":
        if a == 0 and b == 0:
            return 0
        else:
            return 1
    if c == "-":
        if a == 0 and b == 0:
            return 1
        else:
            return 0


def make_operation(matrix, letter, operation):
    global result
    negative = False
    column_index = 0
    for i in range(0, len(matrix[0])):
        if letter.islower():
            negative = True
        if matrix[0][i] == letter.upper():
            column_index = i
    if not result:
        for i in range(1, len(matrix)):
            r = matrix[i][column_index]
            result.append(false_results(negative, r))
        return result
    for i in range(0, len(result)):
        result[i] = logic_operator(
            operation, result[i], false_results(negative, matrix[i + 1][column_index])
        )
    return result


def print_result(matrix):
    matrix[0][-1] = "Func"
    for i in range(0, len(result)):
        matrix[i + 1][-1] = result[i]
    print("\n".join(["".join(["{:4}".format(item) for item in row]) for row in matrix]))


def extract_variables(lista):
    already = []
    for i in range(len(lista)):
        if is_letter(lista[i]):
            if lista[i] not in already:
                already.append(lista[i])
    # already.sort() // maybe, depends on what is more practical
    return already


"""
def unmask_operation(lst):
    global decompiled
    for i in range(len(lst)):
        if lst[i] in ('+', '*', '-', '/'):
            if lst[i - 1] not in decompiled:
                decompiled.append(lst[i - 1])
            decompiled.append(lst[i])
            decompiled.append(lst[i + 1])
"""


def calculate(lista, matrix):
    make_operation(matrix, lista[0], 0)
    for i in range(1, len(lista) - 1, 2):
        make_operation(matrix, lista[i + 1], lista[i])


def check_negative(list):
    temp_index = []
    for i in range(len(list) - 1):
        if list[i] == "!":
            temp_var = list[i + 1]
            list[i + 1] = temp_var.lower()
            temp_index.append(i)
    for i in reversed(range(len(temp_index))):
        list.pop(int(temp_index[i]))


def false_results(negative, a):
    if not negative:
        return a
    if negative:
        if a == 1:
            return 0
        else:
            return 1


def take_of_parenthesis(list):
    counter = 0
    k = 0
    for i in range(len(list)):
        if list[i] == "(":
            counter += 1
    while k < counter:
        temp_index = []
        rn = []
        h = 0
        letter = "a"
        for i in reversed(range(len(list))):
            if list[i] == "(":
                letter = list[i - 1]
                rn.append(i)
                rn.append(i - 1)
                h = i
                break
        while h < len(list):
            if is_letter(list[h]) and not is_letter(list[h - 1]):
                temp_index.append(h)
            if list[h] == ")":
                rn.append(h)
                break
            h += 1
        for j in reversed(range(len(list))):
            if j in rn:
                list.pop(j)
            if j in temp_index:
                list.insert(j + 1, letter)
        k += 1


def separate_letters(list):
    temp_index = []
    for i in range(len(list) - 1):
        if is_letter(list[i]) and is_letter(list[i + 1]):
            temp_index.append(i + 1)
    for i in reversed(range(len(temp_index))):
        list.insert(temp_index[i], "*")


def is_letter(list):
    if list.isalpha():
        return True
    else:
        return False


result = []
user = input("Type yor equation: ")
user_list = list(user)
variables = extract_variables(user_list)
table_of_truth = make_table(variables)
decompiled = user_list.copy()
check_negative(decompiled)
take_of_parenthesis(decompiled)
separate_letters(decompiled)

# unmask_operation(lista)
calculate(decompiled, table_of_truth)
print_result(table_of_truth)

print(user_list)
print(decompiled)
