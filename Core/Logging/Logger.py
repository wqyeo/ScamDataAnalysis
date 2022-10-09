import datetime
from fileinput import filename
from http import server
import os

from multipledispatch import dispatch

from Core.Logging.LogMessage import LogMessage
from Core.Logging.LogSeverity import LogSeverity

def SetupDirectory():
    if not os.path.exists('LogDump'):
        os.mkdir('LogDump')

    dumpPath = os.path.join('LogDump', 'InfoDump')
    if not os.path.exists(dumpPath):
        os.mkdir(dumpPath)

    for logSeverity in LogSeverity:
        dumpSeverityPath = os.path.join(dumpPath, logSeverity.name)
        if not os.path.exists(dumpSeverityPath):
            os.mkdir(dumpSeverityPath)

@dispatch(LogMessage)
def Log(logMessage: LogMessage) -> None:
    SetupDirectory()

    printMessage = "[{logSeverity} {logTitle} :: {logMessage}]".format(
        logSeverity = logMessage.severity.name,
        logTitle = logMessage.title,
        logMessage = logMessage.message
    )
    print(printMessage)
    
    filePath = os.path.join("LogDump", logMessage.GetLogDateString() + ".log")
    with open(filePath, 'a+', encoding="utf-8-sig") as f:
        f.write(logMessage.ToString() + "\r\n")

def DumpInfo(info:str, severity:LogSeverity=LogSeverity.LOG) -> str:
    """
    Dump all info string into a file

    OUTPUT
    --------------------------
    Name of file it has been dumped to.
    """
    SetupDirectory()

    fileName = os.path.join(severity.name, datetime.datetime.now().strftime("%Y-%B-%d_%H-%M-%S_%f") + ".info")
    filePath = os.path.join("LogDump","InfoDump", fileName)
    with open(filePath, 'w', encoding="utf-8-sig") as f:
        f.write(info)

    return fileName

@dispatch(str, str, LogSeverity)
def Log(title:str, message:str, severity:LogSeverity=LogSeverity.LOG) -> None:
    logMessage = LogMessage(title, message, severity)
    Log(logMessage)