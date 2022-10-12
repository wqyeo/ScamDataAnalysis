from turtle import st
from matplotlib import pyplot as plt

from Core.Util import *
from Core.Logging.Logger import *
from Core.Analytics.DataType import DataType

class Chart:
    def __init__(self, savePath: str, jsonData, dataType: DataType) -> None:
        self.savePath = savePath
        self.jsonData = jsonData
        self.dataType = dataType

        self._plotPoints = None
        self._yLabels = None
        self._xLabels = None
        pass

    def Plot(self) -> str:
        if self.dataType == DataType.SCAM_ALERT_STORIES:
            return self._PlotScamAlertStories()
        return None

    def _PlotScamAlertStories(self) -> str:
#region Local_Functions
        def SortDateString(dateStr: str):
            dateStr = dateStr.split(" ")
            year = int(dateStr[0])
            month = Chart._MonthStrToInt(dateStr[1])
            day = int(dateStr[2])

            return (year * 12 * 30) + (month * 30) + day

        def GeneratePlotPointDict() -> dict:
            # NOTE: Key is X-axis, Values are Y-axis
            res = {}

            datesData = self.jsonData["Dates"]
            self._xLabels = []
            for year in datesData:
                for month in datesData[year]:
                    for day in datesData[year][month]:
                        # Increment the case on this particular date by 1
                        dateVal = (int(year) * 12 * 30) + (Chart._MonthStrToInt(month) * 30) + day
                        countVal = res.get(dateVal, 0) + 1
                        res[dateVal] = countVal
                        self._xLabels.append("{y} {m} {d}".format(y=year, m=month, d=str(day)))
            self._xLabels = sorted(self._xLabels, key=SortDateString)
            return res

#endregion

        self._plotPoints = Chart._NormalizePlotPoints(GeneratePlotPointDict())

        xPoints = []
        yPoints = []
        for item in self._plotPoints.items():
            xPoints.append(item[0])
            yPoints.append(item[1])

        plt.plot(xPoints, yPoints)
        ax = plt.axes()
        
        xLabels = xPoints
        if self._xLabels != None:
            xLabels = self._xLabels
        ax.set_xticklabels(xLabels)
        yLabels = yPoints
        if self._yLabels != None:
            yLabels = self._yLabels
        ax.set_yticklabels(yLabels)

        ax.set_xticks(ax.get_xticks()[::3])

        CreateToPath(self.savePath)

        fileName = "DateData.png"
        filePath = os.path.join(self.savePath, fileName)
        plt.savefig(filePath)
        return filePath

    def _MonthStrToInt(monthStr: str) -> int:
        monthStr = monthStr.lower()

        if monthStr == "jan":
            return 1
        elif monthStr == "feb":
            return 2
        elif monthStr == "mar":
            return 3
        elif monthStr == "apr":
            return 4
        elif monthStr == "may":
            return 5
        elif monthStr == "jun":
            return 6
        elif monthStr == "jul":
            return 7
        elif monthStr == "aug":
            return 8
        elif monthStr == "sep":
            return 9
        elif monthStr == "oct":
            return 10
        elif monthStr == "nov":
            return 11
        elif monthStr == "dec":
            return 12
        Log("Failure convert Month String to Int", "Unable to convert the following month string to integer: {}".format(monthStr), LogSeverity.WARNING)
        return 0


    def _NormalizePlotPoints(plotPoints) -> dict:
        """
        Normalize a Plot Point such that the First X axis value begins with a 1
        """
        # Sort by X-axis
        sortedPlotPoints = {key: val for key, val in sorted(plotPoints.items(), key = lambda ele: ele[0])}
        res = {}

        # Normalize the X-axis such that the first X point begins at 1.
        normalizeDiff = None
        for xPoint in sortedPlotPoints:
            if normalizeDiff == None:
                normalizeDiff = xPoint - 1
            res[xPoint - normalizeDiff] = sortedPlotPoints[xPoint]
        return res