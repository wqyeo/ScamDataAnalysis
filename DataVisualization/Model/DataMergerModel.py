import asyncio
from Core.Analytics.Analyzer import Analyzer
from Core.Analytics.DataType import DataType
from Core.Async.TaskThread import TaskThread
from Core.Util import *
from Core.Logging.Logger import *
from Core.Logging.LogSeverity import LogSeverity


class DataMergerModel:
    def __init__(self, viewModelRef) -> None:
        self.viewModelRef = viewModelRef
        pass

    def _StopThread(self, thread: TaskThread):
        if thread != None:
            thread.isRunning = False
        self.viewModelRef.FreeAppThread()


    @asyncio.coroutine
    def MergeData(self, firstFilePath: str, secondFilePath: str, thread: TaskThread = None):
        """
        Tries to analyze data based on the given file path

        ## Output
        List of paths to plot figure. None if invalid analysis. 
        """

#region Local_Function
        def VerifyFilePaths() -> bool:
            nonlocal firstFilePath
            nonlocal secondFilePath
            if not IsValidFilePath(firstFilePath):
                self.ShowUserMessage("First file path is invalid!")
                return False
            if not IsValidFilePath(secondFilePath):
                self.ShowUserMessage("Second file path is invalid!")
                return False
            if firstFilePath == secondFilePath:
                self.ShowUserMessage("First and Second file cannot be the same!")
                return False
            return True
#endregion

        if not VerifyFilePaths():
            Log("Invalid File Path Given", "User gave a possible invalid file path, {} and {}.".format(firstFilePath, secondFilePath), LogSeverity.LOG)
            self._StopThread(thread)
            return

        firstData = Analyzer(firstFilePath, self, thread).AnalyzeData()[0]
        secondData = Analyzer(secondFilePath, self, thread).AnalyzeData()[0]
        merged = None
        try:
            merged = firstData + secondData
        except:
            firstDump = DumpInfo(firstData, LogSeverity.WARNING)
            secondDump = DumpInfo(secondData, LogSeverity.WARNING)
            Log("Merging Data List failed", "Merging both data list failed, more info at {} and {}".format(firstDump, secondDump), LogSeverity.WARNING)
            self.ShowUserMessage("Failed to Merge data.")
            if thread != None:
                thread.isRunning = False
            return None

        try:
            dateTime = datetime.datetime.now().strftime("%Y_%B_%d").strip()
            savePath = GetDirectoryFromFilePath(firstFilePath)
            savePath = os.path.join(savePath, "merged_" + dateTime)
            CreateToPath(savePath)
        except:
            Log("Create Path Failed", "Failure in creating path for saving merged data.}", LogSeverity.ERROR)
            self._StopThread(thread)
            return None

        figurePath = Analyzer(merged, self, thread, savePath).PlotDataFromJson(DataType.MERGED_DATA)
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