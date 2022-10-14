import os
from pathlib import Path

from Core.Logging.Logger import *

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

def IsValidDirectory(filePath: str) -> bool:
    if not filePath.strip():
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

def SortedInsert(list: list, toInsert, comparisonFunc) -> list:
    index = len(list)

    # Find the index to insert into
    for i in range(len(list)):
      if comparisonFunc(list[i], toInsert):
        index = i
        break
 
    # Then insert
    if index == len(list):
      list = list[:index] + [toInsert]
    else:
      list = list[:index] + [toInsert] + list[index:]
    return list

def MonthStrToInt(monthStr: str) -> int:
    monthStr = monthStr.lower()

    if monthStr == "jan":
        return 1
    elif monthStr == "feb":
        return 2
    elif monthStr == "mar":
        return 3
    elif monthStr == "apr":
        return 4
    elif monthStr == "may":
        return 5
    elif monthStr == "jun":
        return 6
    elif monthStr == "jul":
        return 7
    elif monthStr == "aug":
        return 8
    elif monthStr == "sep":
        return 9
    elif monthStr == "oct":
        return 10
    elif monthStr == "nov":
        return 11
    elif monthStr == "dec":
        return 12
    Log("Failure convert Month String to Int", "Unable to convert the following month string to integer: {}".format(monthStr), LogSeverity.WARNING)
    return 0

def Lerp(a: float, b: float, c: float) -> float:
    return (c * a) + ((1.0-c) * b)