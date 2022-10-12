from matplotlib import pyplot as plt

from Core.Logging.Logger import *
from Core.Analytics.DataType import DataType

class Chart:
    def __init__(self, savePath: str, jsonData, dataType: DataType) -> None:
        self.savePath = savePath
        self.jsonData = jsonData
        self.dataType = dataType
        pass

    def Plot(self):
        if self.dataType == DataType.SCAM_ALERT_STORIES:
            self._PlotScamAlertStories()
    

    def _PlotScamAlertStories(self):
#region Local_Functions
        def GeneratePlotPointDict() -> dict:
            # NOTE: Key is X-axis, Values are Y-axis
            res = {}

            datesData = self.jsonData["Dates"]
            for year in datesData:
                for month in datesData[year]:
                    for day in datesData[year][month]:
                        # Increment the case on this particular date by 1
                        dateVal = (int(year) * 12 * 30) + (Chart._MonthStrToInt(month) * 30) + day
                        countVal = res.get(dateVal, 0) + 1
                        res[dateVal] = countVal
            return res

#endregion

        plotPoints = Chart._NormalizePlotPoints(GeneratePlotPointDict())

    def _MonthStrToInt(monthStr: str) -> int:
        monthStr = monthStr.lower()

        if monthStr == "Jan":
            return 1
        elif monthStr == "Feb":
            return 2
        elif monthStr == "Mar":
            return 3
        elif monthStr == "Apr":
            return 4
        elif monthStr == "May":
            return 5
        elif monthStr == "Jun":
            return 6
        elif monthStr == "Jul":
            return 7
        elif monthStr == "Aug":
            return 8
        elif monthStr == "Sep":
            return 9
        elif monthStr == "Oct":
            return 10
        elif monthStr == "Nov":
            return 11
        elif monthStr == "Dec":
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