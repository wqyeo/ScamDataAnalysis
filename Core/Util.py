from operator import truediv


def IsEmptyOrWhitespace(string: str)-> bool:
    if string == None:
        return True
    if string.strip() == "":
        return True
    return False