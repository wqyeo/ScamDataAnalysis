import json
from os import curdir
from Core.Async.TaskThread import TaskThread
from Core.Charting.Chart import Chart

from Core.Util import *
from Core.Analytics.DataType import DataType
from Core.Database import Database
from Core.Logging.LogSeverity import LogSeverity
from Core.Logging.Logger import DumpInfo, Log
from Core.Analytics.WeightingAnalysis import DeterminePlatform, DetermineScamTypes

class Analyzer:
    def __init__(self, filePath: str, appModelRef, thread: TaskThread = None) -> None:
        self.filePath = filePath
        self._appModelRef = appModelRef
        self._fileName = GetFileNameFromPath(filePath)
        self._outputPath = self._CreateFolderPath()
        self._thread = thread

    def AnalyzeData(self):
#region Local_Functions
        def GetAnalyzeDataType(data) -> DataType:
            for d in data:
                if d == "Stories":
                    return DataType.SCAM_ALERT_STORIES
                elif d == "DetailedStories":
                    return DataType.DETAILED_SCAM_ALERT_STORIES
                elif d == "DetailedNews":
                    return DataType.DETAILED_SCAM_ALERT_NEWS
                elif d == "News":
                    return DataType.SCAM_ALERT_NEWS
            return None
        
        def PlotData(data, dataType: DataType, plotPath: str) -> bool:
            plotted = False
            if analyzeData != None:
                chart = Chart(plotPath, data, dataType, self._thread)
                plotted = chart.Plot()
            return plotted

        def TrySaveData(savePath, data) -> bool:
            try:
                CreateToPath(savePath)
                filePath = os.path.join(savePath, "analysis_data.json")
                Database.SaveJsonData(data, filePath)
                return True
            except Exception as e:
                Log("Save Analysis Data Failed", "Failed to save analyzed data, {}".format(getattr(e, 'message', repr(e))), LogSeverity.WARNING)
                return False
#endregion

        jsonData = None
        try:
            jsonData = Database.OpenJsonData(self.filePath)
            
            dataType = GetAnalyzeDataType(jsonData)
            if dataType == None:
                raise Exception("Invalid JSON Data")
        except:
            Log("Error Convering Json File", "Error Converting JSON File from path {}.".format(self.filePath), LogSeverity.WARNING)
            return None

        self._appModelRef.ShowUserMessage("")
        analyzeData = None
        if dataType == DataType.SCAM_ALERT_STORIES or dataType == DataType.SCAM_ALERT_NEWS:
            self._appModelRef.ShowUserMessage("NOTE: Crawling Undetailed Data.\nThere will be lesser data generated.\nTo generate more data, use the deep data crawler on this current data and perform analysis on it.")
            analyzeData = self._BundleSimpleData(jsonData)
        elif dataType == DataType.DETAILED_SCAM_ALERT_STORIES:
            analyzeData = self._BundleDetailedScamAlertStories(jsonData)
        elif dataType == DataType.DETAILED_SCAM_ALERT_NEWS:
            analyzeData = self._BundleDetailedScamAlertNews(jsonData)

        if analyzeData == None:
            Log("Data failed to Bundle", "Failed to bundle Data for file {}.".format(self.filePath), LogSeverity.WARNING)
            return None

        chartPaths = os.path.join(self._outputPath, "charts")
        TrySaveData(chartPaths, analyzeData)
        
        if PlotData(analyzeData, dataType, chartPaths):
            figuresPath = []
            # Get all plot figures (.png)
            for file in os.listdir(chartPaths):
                if file.endswith(".png"):
                    t = os.path.join(chartPaths, file)
                    figuresPath.append(t)
            return figuresPath
        self._appModelRef.ShowUserMessage("The Data given is either invalid or doesn't exists.")
        return None

    def _CreateFolderPath(self) -> str:
        path = GetDirectoryFromFilePath(self.filePath)
        path = os.path.join(path, GetFileNameFromPath(self.filePath))
        CreateToPath(path)
        return path

    def _BundleDetailedScamAlertNews(self, jsonData) -> dict:
        jsonData = jsonData["DetailedNews"]
        resultData = []

        for data in jsonData:
            if data == None:
                continue

            currData = {
                "Dates": None,
                "ScamTypes": [],
                "PlatformTypes": None
            }
            warnMissingData = False

            if "Date" in data:
                currData["Dates"] = data["Date"]

            if "Description" in data:
                platform = DeterminePlatform(data["Description"])
                currData["PlatformTypes"] = platform

                scamTypes = DetermineScamTypes(data["Description"])
                currData["ScamTypes"] = scamTypes

                if platform == "Unknown":
                    LogAndDump("Unknown Platform Detected", "Unknown platform detected for description.", data["Description"])

            if currData["Dates"] == None or len(currData["ScamTypes"]) == 0 or currData["PlatformTypes"] == None:
                warnMissingData = True

            if warnMissingData:
                dumpPath = DumpInfo(json.dumps(data), LogSeverity.WARNING)
                Log("Missing Data in given JSON", "Missing data in user given JSON, more Info at {}".format(dumpPath), LogSeverity.WARNING)
            else:
                resultData.append(currData)
        return resultData

    def _BundleDetailedScamAlertStories(self, jsonData) -> dict:
        jsonData = jsonData["DetailedStories"]

        resultData = []

        for data in jsonData:
            if data == None:
                continue
            currData = {
                "Dates": None,
                "ScamTypes": [],
                "PlatformTypes": None
            }

            titleAuthor = data.get("TitleAuthor", {})
            body = data.get("Body", {})
            warnMissingData = False
            
            if titleAuthor != None:
                # Date
                if "Date" in titleAuthor:
                    dateStr = titleAuthor["Date"]
                    currData["Dates"] = dateStr
                else:
                    warnMissingData = True
            else:
                warnMissingData = True

            if body != None:
                # Scam Type
                if "ScamType" in body:
                    scamTypes = body["ScamType"]
                    if isinstance(scamTypes, list):
                        # This data is in multiple scam category
                        for scamType in scamTypes:
                            currData["ScamTypes"].append(scamType)
                    else:
                        currData["ScamTypes"].append(scamTypes)
                else:
                    warnMissingData = True

                # Determine the platform the scam was performed on
                # by reading the description.
                if "Description" in body:
                    scamDesc = body["Description"]
                    platform = DeterminePlatform(scamDesc)
                    currData["PlatformTypes"] = platform

                    # NOTE: Logging
                    if platform == "Unknown":
                        LogAndDump("Unknown Platform Detected", "Unknown platform detected for description.", scamDesc)
                else:
                    warnMissingData = True
            else: 
                warnMissingData = True

            if warnMissingData:
                dumpPath = DumpInfo(json.dumps(data), LogSeverity.WARNING)
                Log("Missing Data in given JSON", "Missing data in user given JSON, more Info at {}".format(dumpPath), LogSeverity.WARNING)
            else:
                resultData.append(currData)
        return resultData

    def _BundleSimpleData(self, jsonData) -> dict:

        if "Stories" in jsonData:
            jsonData = jsonData["Stories"]
        elif "News" in jsonData:
            jsonData = jsonData["News"]
        else:
            return None

        resultData = []

        for data in jsonData:
            currData = {}
            if "Date" in data:
                currData["Dates"] = data["Date"]
                resultData.append(currData)
            else:
                dumpPath = DumpInfo(json.dumps(data), LogSeverity.WARNING)
                Log("Missing Data in given JSON", "Missing data in user given JSON, more Info at {}".format(dumpPath), LogSeverity.WARNING)
        return resultData