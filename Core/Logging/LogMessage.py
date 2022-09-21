import datetime

from Core.Logging.LogSeverity import LogSeverity

class LogMessage:
    def __init__(self, title:str, message:str, severity:LogSeverity) -> None:
        self.title = title
        self.message = message
        self.severity = severity
        self.date= datetime.datetime.now()
        pass

    def ToString(self) -> str:
        result = "[{logDate}] ({logSeverity}) {logTitle} :: {logMessage}"
        return result.format(
            # Timezone Date HourMinute
            logDate = self.date.strftime("%Z%z %Y-%B-%d %X"),
            logSeverity = self.severity.name,
            logTitle = self.title,
            logMessage = self.message
        )

    def GetLogDateString(self) -> str:
        return self.date.strftime("%Y-%B-%d")