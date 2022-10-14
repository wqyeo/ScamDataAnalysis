from dataclasses import dataclass
from Core.Charting.DataCategory import DataCategory
from Core.Charting.Point import Point
from Core.Logging.Logger import *

from Core.Util import *

class Data:
    def __init__(self, dataCategory: DataCategory):
        """
        **dataFilter**
        A function that takes in data.
        If true, the data will not be processed.
        """
        self.dataCategory = dataCategory
        self.points = []
        
        self._normalizedDiff = None
        self._cumulative = 0
        self._countableMappings = {}
        self.dataSize = 0

    def AppendData(self, data):

        if self.dataCategory == DataCategory.DATE:
            self._AppendDate(data)
        elif self.dataCategory == DataCategory.DATE_OVER_TIME:
            self._AppendDateOverTime(data)
        elif self.dataCategory == DataCategory.COUNTABLES:
            self._AppendCountable(data)
        self.dataSize += 1

    def _AppendCountable(self, data):
        if isinstance(data, list):
            for d in data:
                self._AppendCountable(d)
                return None

        # NOTE: Y would be the value to count
        # X will be the number of occurance
        yValueMap = None
        if data in self._countableMappings:
            yValueMap = self._countableMappings[data]
        else:
            self._cumulative += 1
            self._countableMappings[data] = self._cumulative
            yValueMap = self._cumulative

        point = self._FindPointByY(yValueMap)
        if point == None:
            point = Point(1, yValueMap, yLabel=data)
            self.points.append(point)
        else:
            point.xValue += 1

    def _AppendDateOverTime(self, date):
        self._cumulative += 1
        
        rawValue = Data._GetDateRawValue(date)
        if self._normalizedDiff == None:
            self._normalizedDiff = rawValue - 1
        rawValue = rawValue - self._normalizedDiff

        point = self._FindPointByX(rawValue)
        if point == None:
            point = Point(rawValue, self._cumulative, xLabel=date)
            self.points.append(point)
        else:
            point.yValue = self._cumulative

    def _AppendDate(self, date):
        rawValue = Data._GetDateRawValue(date)
        if self._normalizedDiff == None:
            self._normalizedDiff = rawValue - 1
        rawValue = rawValue - self._normalizedDiff

        point = self._FindPointByX(rawValue)
        if point == None:
            point = Point(rawValue, 1, xLabel=date)
            self.points.append(point)
        else:
            point.yValue += 1

    def _FindPointByY(self, yValue: int) -> Point:
        for p in self.points:
            if p.yValue == yValue:
                return p
        return None

    def _FindPointByX(self, xValue: int) -> Point:
        for p in self.points:
            if p.xValue == xValue:
                return p
        return None

    def _GetDateRawValue(dateStr: str) -> int:
        dateStr = dateStr.split()
    
        year = int(dateStr[2])
        month = MonthStrToInt(dateStr[1])
        day = int(dateStr[0])
        return (year * 30 * 12) + (month * 30) + day

    def Size(self) -> int:
        return len(self.points)