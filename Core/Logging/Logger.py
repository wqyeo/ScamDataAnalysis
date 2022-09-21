import datetime
import os

from multipledispatch import dispatch

from Core.Logging.LogMessage import LogMessage
from Core.Logging.LogSeverity import LogSeverity

def SetupDirectory():
    if not os.path.exists('LogDump'):
        os.mkdir('LogDump')

    if not os.path.exists('LogDump/InfoDump'):
        os.mkdir('LogDump/InfoDump')

@dispatch(LogMessage)
def Log(logMessage: LogMessage) -> None:
    SetupDirectory()

    print(logMessage.title + " : " + logMessage.message)
    
    filePath = "LogDump/" + logMessage.GetLogDateString() + ".log"
    with open(filePath, 'a+') as f:
        f.write(logMessage.ToString() + "\r\n")

def DumpInfo(info:str) -> str:
    """
    Dump all info string into a file

    OUTPUT
    --------------------------
    Name of file it has been dumped to.
    """
    SetupDirectory()

    fileName = "InfoDump/" + datetime.datetime.now().strftime("%Y-%B-%d_%H-%M-%S_%f") + ".info"
    filePath = "LogDump/" + fileName
    with open(filePath, 'w') as f:
        f.write(info)

    return fileName

@dispatch(str, str, LogSeverity)
def Log(title:str, message:str, severity:LogSeverity=LogSeverity.LOG) -> None:
    logMessage = LogMessage(title, message, severity)
    Log(logMessage)