from Core.Charting.DataCategory import DataCategory
from Core.Charting.Point import Point
from Core.Logging.Logger import *

from Core.Util import *

class Data:
    def __init__(self, dataCategory: DataCategory):
        self.dataCategory = dataCategory
        self.points = []
        self._normalizedDiff = None

    def AppendData(self, data):
        if self.dataCategory == DataCategory.DATE:
            self._AppendDate(data)
            pass

    def Size(self) -> int:
        return len(self.points)

    def _AppendDate(self, date):
#region Local_Function
        def GetDateRawValue(dateStr: str) -> int:
            dateStr = dateStr.split()
        
            year = int(dateStr[2])
            month = MonthStrToInt(dateStr[1])
            day = int(dateStr[0])
            return (year * 30 * 12) + (month * 30) + day
#endregion

        rawValue = GetDateRawValue(date)
        if self._normalizedDiff == None:
            self._normalizedDiff = rawValue - 1
        rawValue = rawValue - self._normalizedDiff

        point = self._FindPointByX(rawValue)
        if point == None:
            point = Point(rawValue, 1, xLabel=date)
            self.points.append(point)
        else:
            point.yValue += 1

    def _FindPointByX(self, xValue: int) -> Point:
        for p in self.points:
            if p.xValue == xValue:
                return p
        return None
