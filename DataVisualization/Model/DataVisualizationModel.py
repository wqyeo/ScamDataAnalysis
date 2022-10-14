import asyncio
from Core.Analytics.Analyzer import Analyzer
from Core.Async.TaskThread import TaskThread
from Core.Util import *
from Core.Logging.Logger import *
from Core.Logging.LogSeverity import LogSeverity


class DataVisualizationModel:
    def __init__(self, viewModelRef) -> None:
        self.viewModelRef = viewModelRef
        pass

    @asyncio.coroutine
    def AnalyzeData(self, filePath, thread: TaskThread = None):
        """
        Tries to analyze data based on the given file path

        ## Output
        List of paths to plot figure. None if invalid analysis. 
        """

        if not IsValidFilePath(filePath):
            Log("Invalid File Path Given", "User gave a possible invalid file path, {}.".format(filePath), LogSeverity.WARNING)
            if thread != None:
                thread.isRunning = False
            return

        dataAnalyzer = Analyzer(filePath, self, thread)
        figurePath = dataAnalyzer.AnalyzeData()

        if thread != None:
            # Thread ended due to signal stop. So we return none
            if not thread.isRunning:
                figurePath = None
            else:
                thread.isRunning = False
            self.viewModelRef.FreeAppThread()
            
        self.viewModelRef.SetFigurePaths(figurePath)

    def ShowUserMessage(self, message: str) -> None:
        self.viewModelRef.ShowUserMessage(message)