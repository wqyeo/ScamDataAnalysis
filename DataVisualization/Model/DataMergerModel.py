import asyncio
from xml.etree.ElementTree import TreeBuilder
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

    def _DoMerge(self, firstFilePath: str, secondFilePath: str, thread: TaskThread = None):
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

        def TryCreateSavePath() -> bool:
            nonlocal firstFilePath
            nonlocal thread
            savePath = None
            try:
                dateTime = datetime.datetime.now().strftime("%Y_%B_%d").strip()
                savePath = GetDirectoryFromFilePath(firstFilePath)
                savePath = os.path.join(savePath, "merged_" + dateTime)
                CreateToPath(savePath)
            except:
                Log("Create Path Failed", "Failure in creating path for saving merged data.}", LogSeverity.ERROR)
                self._StopThread(thread)
                savePath = None
            return savePath

        def TryMergeData(firstData, secondData):
            nonlocal thread

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
            return merged

        def TryAnalyzeData(filePath: str):
            nonlocal thread
            data = None
            try:
                data = Analyzer(filePath, self, thread).AnalyzeData()[0]
            except Exception as e:
                Log("Failed to analyze data", "Failed to analyze data on path {p}. Error Message: {e}".format(p=filePath, e=getattr(e, 'message', repr(e))), LogSeverity.SEVERE)
                self.viewModelRef.ShowUserMessage("Failed to analyze data on {}.".format(filePath))
            return data

#endregion

        if not VerifyFilePaths():
            Log("Invalid File Path Given", "User gave a possible invalid file path, {} and {}.".format(firstFilePath, secondFilePath), LogSeverity.LOG)
            self._StopThread(thread)
            return

        
        
        firstData = TryAnalyzeData(firstFilePath)
        secondData = TryAnalyzeData(secondFilePath)
        if firstData == None or secondData == None:
            return None
        merged = TryMergeData(firstData, secondData)

        savePath = TryCreateSavePath()
        if savePath == None:
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

    @asyncio.coroutine
    def MergeData(self, firstFilePath: str, secondFilePath: str, thread: TaskThread = None):
        """
        Tries to analyze data based on the given file path

        ## Output
        List of paths to plot figure. None if invalid analysis. 
        """
        try:
            self._DoMerge(firstFilePath, secondFilePath, thread)
        except Exception as e:
            Log("Unhandled DeepCrawlerModel Exception", "Unhandled exception, {}".format(getattr(e, 'message', repr(e))), LogSeverity.SEVERE)
            self.viewModelRef.ShowUserMessage("Woops, a severe error occured! Check LogDump for more info.")
        finally:
            if thread != None:
                thread.isRunning = False
                self.viewModelRef.FreeAppThread()

    def ShowUserMessage(self, message: str) -> None:
        self.viewModelRef.ShowUserMessage(message)