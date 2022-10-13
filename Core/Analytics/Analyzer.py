import json
from logging import logMultiprocessing
from Core.Charting.Chart import Chart

from Core.Util import *
from Core.Analytics.DataType import DataType
from Core.Database import Database
from Core.Logging.LogSeverity import LogSeverity
from Core.Logging.Logger import DumpInfo, Log

class Analyzer:
    def __init__(self, filePath: str) -> None:
        self.filePath = filePath
        self._fileName = GetFileNameFromPath(filePath)
        self._outputPath = self._CreateFolderPath()

    def AnalyzeData(self) -> logMultiprocessing:
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

            # TODO: Allow loading from other data types
            if not ('Stories' in jsonData):
                raise Exception("JSON Format Invalid")
            
            dataType = GetAnalyzeDataType(jsonData)
            if dataType == None:
                raise Exception("Invalid JSON Data")
        except:
            Log("Error Convering Json File", "Error Converting JSON File from path {}.".format(self.filePath), LogSeverity.WARNING)
            return None

        analyzeData = None
        if dataType == DataType.SCAM_ALERT_STORIES:
            analyzeData = self._CrawlScamAlertStories(jsonData)

        chartPaths = os.path.join(self._outputPath, "charts")
        if PlotData(analyzeData, dataType, chartPaths):
            figuresPath = []
            # Get all plot figures (.png)
            for file in os.listdir(chartPaths):
                if file.endswith(".png"):
                    t = os.path.join(chartPaths, file)
                    figuresPath.append(t)
            return figuresPath
        return None

    def _CreateFolderPath(self) -> str:
        path = GetDirectoryFromFilePath(self.filePath)
        path = os.path.join(path, GetFileNameFromPath(self.filePath))
        CreateToPath(path)
        return path

    def _CrawlScamAlertStories(self, jsonData) -> dict:

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