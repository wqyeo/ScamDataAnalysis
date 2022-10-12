import os
from pathlib import Path

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

def GetFileNameFromPath(filePath: str, withExtension: bool = False) -> str:
    if withExtension:
        return Path(filePath).name
    return Path(filePath).stem

def CreateToPath(filePath: str) -> bool:
    if not os.path.exists(filePath):
        os.makedirs(filePath)
        return True
    return False