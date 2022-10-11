import os

from operator import truediv


def IsEmptyOrWhitespace(string: str)-> bool:
    if string == None:
        return True
    if string.strip() == "":
        return True
    return False

def IsValidFilePath(filePath: str) -> bool:
    if not filePath.strip():
        return False
    if not os.path.isfile(filePath):
        return False
    return True

def GetDirectoryFromFilePath(filePath: str) -> str:
    return os.path.dirname(os.path.abspath(filePath))