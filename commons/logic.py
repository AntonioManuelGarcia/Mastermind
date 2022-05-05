from random import randint

VALID_GUEST_VALUES = ['R', 'G', 'B', 'Y', 'W', 'O']


def createcode():
    code = ""
    for x in range(4):
        code += VALID_GUEST_VALUES[randint(0, 5)]
    return code


def checkguestvalue(val):
    valid = False
    if val in VALID_GUEST_VALUES:
        valid = True
    return valid


def checkvalidguest(guest):
    valid = False
    if checkguestvalue(guest[0]) and checkguestvalue(guest[1]) \
            and checkguestvalue(guest[2]) and checkguestvalue(guest[3]):
        valid = True
    return valid


def checkguestformat(guest):
    try:
        if len(guest) == 4 and checkvalidguest(guest):
            return True
        else:
            return False
    except Exception:
        return False


def checkblacks(guest, code):
    blacks = 0
    for x in range(4):
        if guest[x] == code[x]:
            blacks += 1
    return blacks


def checkwhites(guest, code):
    non_blacks = []
    non_blacks_code = []
    whites = 0
    for x in range(4):
        if not guest[x] == code[x]:
            non_blacks.append(guest[x])
            non_blacks_code.append(code[x])
    for x in non_blacks:
        if x in non_blacks_code:
            non_blacks_code.remove(x)
            whites += 1
    return whites
