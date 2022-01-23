class Triad(object):
    def __init__(self, operation=None, operands=[]):
        self.operation = operation
        self.operands = operands

    def set_Operation(self, operation):
        self.operation = operation

    def set_Operands(self, operand):
        self.operands.append(operand)

    def __repr__(self):
        return ' ' + str(self.operation) + ' : ' + str(self.operands)


def POLICtoTriad(POLIC):
    Triads = []
    cop_POLIC = POLIC.copy()
    log_op = ['==', '!=', '>', '>=', '<', '<=']
    op = ['+', '-', '*', '/', '=']

    i = 0
    while len(POLIC):
        if '!' in POLIC[0]:
            if int(POLIC[0][1:]) < cop_POLIC.index(POLIC[0]):
                k = 1
                for j in range(int(POLIC[i][1:]) - cop_POLIC.index(POLIC[i])):
                    if POLIC[j] in op:
                        k += 1
                    elif POLIC[j] in log_op:
                        k += 2
                Triads.append(Triad('jump', ['None', '^' + str(len(Triads) - k)]))
                POLIC.pop(0)
            else:
                flag = True
                for item in Triads:
                    if '^' + str(POLIC[0])[1:] in item.operands:
                        Triads.append(Triad('jump', ['None', '^' + str(Triads.index(item))]))
                        flag = False
                        break

                if flag:
                    k = 1
                    for j in range(int(POLIC[i][1:]) - cop_POLIC.index(POLIC[i])):
                        if POLIC[j] in op:
                            k += 1
                        elif POLIC[j] in log_op:
                            k += 2

                    Triads.append(Triad('jump', ['None', '^' + str(len(Triads) + k)]))
                    POLIC.pop(0)
                    if len(POLIC):
                        if (str(type(POLIC[0]))) == "<class 'int'>":
                            POLIC.pop(0)
                else:
                    POLIC.pop(0)

        if len(POLIC) > 2:
            if POLIC[i] in op:
                if POLIC[1] in op:
                    Triads.append(Triad(POLIC[1], [POLIC[0], '^' + str(len(Triads) - 1)]))
                    POLIC.pop(0)
                    POLIC.pop(0)
                    i -= 2
                else:
                    Triads.append(Triad(POLIC[i], [POLIC[i - 2], POLIC[i - 1]]))
                    POLIC.pop(i - 2)
                    POLIC.pop(i - 2)
                    POLIC.pop(i - 2)
                    i -= 3

            elif POLIC[i] in log_op:
                Triads.append(Triad(POLIC[i], [POLIC[i - 2], POLIC[i - 1]]))
                POLIC.pop(i - 2)
                POLIC.pop(i - 2)
                POLIC.pop(i - 2)
                i -= 2

                k = 1
                for j in range(POLIC[i] - cop_POLIC.index(POLIC[i])):
                    if POLIC[j] in op:
                        k += 1
                    elif POLIC[j] in log_op:
                        k += 2

                if POLIC[i] < len(cop_POLIC):
                    if '!' in cop_POLIC[POLIC[i]]:
                        k += 2

                Triads.append(Triad('if', ['^' + str(len(Triads) - 1), '^' + str(len(Triads) + k)]))
                POLIC.pop(0)
                i -= 1

        elif len(POLIC) == 2:
            Triads.append(Triad(POLIC[1], [POLIC[0], '^' + str(len(Triads) - 1)]))
            POLIC.pop(0)
            POLIC.pop(0)

        i += 1

    print(Triads)
    Optimazator(Triads)
    print(Triads)
    return TriadtoPOLIC(Triads)


def Optimazator(Triads):
    op = ['+', '-', '*', '/', '=']
    deletes = []
    del_Trids = []

    for i in range(len(Triads)):
        if Triads[i].operation == '=':
            for j in range(i + 1, len(Triads)):
                if Triads[i].operands[0] in Triads[j].operands:
                    if Triads[j].operation == '=' and not j == len(Triads) - 1:
                        if Triads[i].operands[0] not in Triads[int(Triads[j].operands[1][1:])].operands:
                            deletes.append(i)

    for i in deletes:
        for j in Triads[int(i)].operands:
            if '^' in j:
                deletes.append(j[1:])

    deletes = list(map(int, deletes))

    for i in deletes:
        del_Trids.append(Triads[i])

    for i in del_Trids:
        index = Triads.index(i)
        for j in range(index, len(Triads)):
            if '^' in Triads[j].operands[0] or '^' in Triads[j].operands[1]:
                if Triads[j].operation == 'if':
                    Triads[j].operands[0] = '^' + str(int(Triads[j].operands[0][1:]) - 1)
                    Triads[j].operands[1] = '^' + str(int(Triads[j].operands[1][1:]) - 1)
                else:
                    Triads[j].operands[1] = '^' + str(int(Triads[j].operands[1][1:]) - 1)
        Triads.remove(i)

    k = 0
    r = 0
    deletes = []
    del_Trids = []
    for i in range(len(Triads)):
        if Triads[i].operation in op:
            if Triads[i].operands[0].isdigit() and Triads[i].operands[1].isdigit():
                k = i
                r = sum(map(int, Triads[i].operands))
                for j in range(i, len(Triads)):
                    if '^' + str(k) in Triads[j].operands:
                        Triads[j].operands[1] = str(r)
                        deletes.append(k)

    deletes = list(map(int, deletes))
    for i in deletes:
        del_Trids.append(Triads[i])

    for i in del_Trids:
        index = Triads.index(i)
        for j in range(index, len(Triads)):
            if '^' in Triads[j].operands[0] or '^' in Triads[j].operands[1]:
                if Triads[j].operation == 'if':
                    Triads[j].operands[0] = '^' + str(int(Triads[j].operands[0][1:]) - 1)
                    Triads[j].operands[1] = '^' + str(int(Triads[j].operands[1][1:]) - 1)
                else:
                    Triads[j].operands[1] = '^' + str(int(Triads[j].operands[1][1:]) - 1)
        Triads.remove(i)


def TriadtoPOLIC(Triads):
    POLIC = []
    k = 0
    g = 0

    for triad in Triads:
        if triad.operation == '=':
            POLIC.append(triad.operands[0])
            POLIC.append(triad.operands[1])
            POLIC.append(triad.operation)

        if triad.operation == 'if':
            t = Triads[int(triad.operands[0][1:])]
            POLIC.append(t.operands[0])
            POLIC.append(t.operands[1])
            POLIC.append(t.operation)
            k += 1
            POLIC.append('{' + str(k) + '}')

        if triad.operation == 'jump':
            if int(triad.operands[1][1:]) == len(Triads):
                g += 1
                POLIC.append('{' + str(g) + '}')
            elif int(triad.operands[1][1:]) < len(Triads):
                index = POLIC.index('{' + str(k) + '}')
                POLIC.append('!'+str(index - 3))

            index = POLIC.index('{' + str(k) + '}')
            POLIC.insert(index, len(POLIC) + 1)
            POLIC.pop(index + 1)
            k -= 1

    flag = True
    while flag:
        flag = False
        for i in POLIC:
            if '^' in str(i):
                flag = True

        for i in POLIC:
            if '^' in str(i):
                index = POLIC.index(i)
                t = Triads[int(i[1:])]
                POLIC.insert(index, t.operands[0])
                POLIC.insert(index + 1, t.operands[1])
                POLIC.insert(index + 2, t.operation)
                POLIC.pop(index + 3)
                break

    if '{' + str(k) + '}' in POLIC:
        index = POLIC.index('{' + str(k) + '}')
        POLIC.insert(index, len(POLIC))
        POLIC.pop(index + 1)

    if '{' + str(g) + '}' in POLIC:
        index = POLIC.index('{' + str(g) + '}')
        POLIC.insert(index, '!' + str(len(POLIC) + 1))
        POLIC.insert(index + 1, len(POLIC))
        POLIC.pop(index + 2)

    return POLIC
