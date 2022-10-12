import json
import matplotlib.pyplot as plt

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

    def AnalyzeData(self) -> bool:
#region Local_Functions
        def truncateKeys(datecount, length):
            return dict((k[6:length], v) for k, v in datecount.items())

        def GetAnalyzeDataType(data) -> DataType:
            for d in data:
                if d == "Stories":
                    return DataType.SCAM_ALERT_STORIES
                elif d == "DetailedStories":
                    return DataType.DETAILED_SCAM_ALERT_STORIES
            return None
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
            return False

        if dataType == DataType.SCAM_ALERT_STORIES:
            return self._CrawlScamAlertStories(jsonData)

        dateData = []
        for data in jsonData:
            if 'Date' in data:
                dateData.append(data["Date"])

        dateCount = {}
        for i in dateData:
            t = dateCount.get(i, 0) + 1
            dateCount[i] = t
        dateCount = dict(sorted(dateCount.items()))

        shortendate = truncateKeys(dateCount, -4)

        # TODO: Find a way to output plot
        # Plotting
        xAxis = [key for key, value in shortendate.items()]
        yAxis = [value for key, value in shortendate.items()]
        plt.grid(True)

        ## LINE GRAPH ##
        plt.plot(xAxis, yAxis, color='maroon', marker='o')
        plt.xlabel('Date')
        plt.ylabel('Number of Scam Cases')

        ## BAR GRAPH ##
        # fig = plt.figure()
        # plt.bar(xAxis, yAxis, color='maroon')
        # plt.xlabel('Date')
        # plt.ylabel('Number of Scam Cases')

        plt.savefig(self.outputPath)
        return True

    def _CreateFolderPath(self) -> str:
        path = GetDirectoryFromFilePath(self.filePath)
        path = os.path.join(path, GetFileNameFromPath(self.filePath))
        CreateToPath(path)
        return path

    def _CrawlScamAlertStories(self, jsonData):
#region Local_Function
        def AppendDateToDict(dict: dict, year: str, month: str, day: str) -> None:
            # Fetch
            yearDict = dict["Dates"].get(year, {})
            monthArr = yearDict.get(month, [])
            # Append to fetched, then bind.
            monthArr.append(int(day))
            yearDict[month] = monthArr
            dict["Dates"][year] = yearDict

#endregion


        jsonData = jsonData["Stories"]

        resultData = json.loads('{"Dates": {}}')

        for data in jsonData:
            if "Date" in data:
                dateStr = data["Date"]
                dateStr = dateStr.split()
                
                year = dateStr[2]
                month = dateStr[1]
                day = dateStr[0]

                AppendDateToDict(resultData, year, month, day)
            else:
                dumpPath = DumpInfo(json.dumps(data), LogSeverity.WARNING)
                Log("Missing Data in given JSON", "Missing data in user given JSON, more Info at {}".format(dumpPath), LogSeverity.WARNING)

        fileName = "Data.json"
        savePath = os.path.join(self._outputPath, fileName)
        Database.SaveJsonData(resultData, savePath)
        return True