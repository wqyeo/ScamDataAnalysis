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

    def _DoAnalyze(self, filePath, thread: TaskThread = None):
        if not IsValidFilePath(filePath):
            Log("Invalid File Path Given", "User gave a possible invalid file path, {}.".format(filePath), LogSeverity.WARNING)
            if thread != None:
                thread.isRunning = False
            return

        dataAnalyzer = Analyzer(filePath, self, thread)
        figurePath = dataAnalyzer.PlotData()

        if thread != None:
            # Thread ended due to signal stop. So we return none
            if not thread.isRunning:
                figurePath = None
            else:
                thread.isRunning = False
            self.viewModelRef.FreeAppThread()
            
        self.viewModelRef.SetFigurePaths(figurePath)
        
    @asyncio.coroutine
    def AnalyzeData(self, filePath, thread: TaskThread = None):
        """
        Tries to analyze data based on the given file path

        ## Output
        List of paths to plot figure. None if invalid analysis. 
        """
        try:
            self._DoAnalyze(filePath, thread)
        except Exception as e:
            Log("Unhandled CrawlerModel Exception", "Unhandled exception, {}".format(getattr(e, 'message', repr(e))), LogSeverity.SEVERE)
            self.viewModelRef.ShowUserMessage("Woops, a severe error occured! Check LogDump for more info.")
        finally:
            if thread != None:
                thread.isRunning = False
                self.viewModelRef.FreeAppThread()
    
    def ShowUserMessage(self, message: str) -> None:
        self.viewModelRef.ShowUserMessage(message)