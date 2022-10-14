import json
from Core.Charting.Chart import Chart

from Core.Util import *
from Core.Analytics.DataType import DataType
from Core.Database import Database
from Core.Logging.LogSeverity import LogSeverity
from Core.Logging.Logger import DumpInfo, Log
from Core.Analytics.WeightingAnalysis import DeterminePlatform

class Analyzer:
    def __init__(self, filePath: str, appModelRef) -> None:
        self.filePath = filePath
        self._appModelRef = appModelRef
        self._fileName = GetFileNameFromPath(filePath)
        self._outputPath = self._CreateFolderPath()

    def AnalyzeData(self):
#region Local_Functions
        def GetAnalyzeDataType(data) -> DataType:
            for d in data:
                if d == "Stories":
                    return DataType.SCAM_ALERT_STORIES
                elif d == "DetailedStories":
                    return DataType.DETAILED_SCAM_ALERT_STORIES
            return None
        
        def PlotData(data, dataType: DataType, plotPath: str) -> bool:
            plotted = False
            if analyzeData != None:
                chart = Chart(plotPath, data, dataType)
                plotted = chart.Plot()
            return plotted
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

        analyzeData = None
        if dataType == DataType.SCAM_ALERT_STORIES:
            self._appModelRef.ShowUserMessage("NOTE: Crawling Undetailed Data.\nThere will be lesser data generated.\nTo generate more data, use the deep data crawler on this current data and perform analysis on it.")
            analyzeData = self._BundleScamAlertStories(jsonData)
        elif dataType == DataType.DETAILED_SCAM_ALERT_STORIES:
            self._appModelRef.ShowUserMessage("")
            analyzeData = self._BundleDetailedScamAlertStories(jsonData)

        chartPaths = os.path.join(self._outputPath, "charts")
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

    def _BundleDetailedScamAlertStories(self, jsonData) -> dict:

        jsonData = jsonData["DetailedStories"]

        resultData = {
            "Dates": [],
            "ScamTypes": [],
            "PlatformTypes": []
        }

        for data in jsonData:
            titleAuthor = data.get("TitleAuthor", {})
            body = data.get("Body", {})
            warnMissingData = False
            
            # Append Date
            if "Date" in titleAuthor:
                dateStr = titleAuthor["Date"]
                resultData["Dates"].append(dateStr)
            else:
                warnMissingData = True

            # Scam Type
            if "ScamType" in body:
                scamTypes = body["ScamType"]
                if isinstance(scamTypes, list):
                    # This data is in multiple scam category
                    for scamType in scamTypes:
                        resultData["ScamTypes"].append(scamType)
                else:
                    resultData["ScamTypes"].append(scamTypes)
            else:
                warnMissingData = True

            # Determine the platform the scam was performed on
            # by reading the description.
            if "Description" in body:
                scamDesc = body["Description"]
                platform = DeterminePlatform(scamDesc)
                resultData["PlatformTypes"].append(platform)
            else:
                warnMissingData = True

            if warnMissingData:
                dumpPath = DumpInfo(json.dumps(data), LogSeverity.WARNING)
                Log("Missing Data in given JSON", "Missing data in user given JSON, more Info at {}".format(dumpPath), LogSeverity.WARNING)
        return resultData

    def _BundleScamAlertStories(self, jsonData) -> dict:

        jsonData = jsonData["Stories"]

        resultData = {
            "Dates": []
        }

        for data in jsonData:
            if "Date" in data:
                dateStr = data["Date"]
                resultData["Dates"].append(dateStr)
            else:
                dumpPath = DumpInfo(json.dumps(data), LogSeverity.WARNING)
                Log("Missing Data in given JSON", "Missing data in user given JSON, more Info at {}".format(dumpPath), LogSeverity.WARNING)
        return resultData