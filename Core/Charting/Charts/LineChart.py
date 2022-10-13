from Core.Charting.Charts.VisualChart import VisualChart
from Core.Charting.Data import Data

class LineChart(VisualChart):
    def __init__(self, title, data: Data):
        self.xValues = []
        self.yValues = []
        self.xLabels = []
        self.yLabels = []
        
        self.UnpackData(data)
        super().__init__(title)

    def UnpackData(self, data: Data):
        for point in data.points:
            self.xValues.append(point.xValue)
            self.yValues.append(point.yValue)

            if point.yLabel == None:
                self.yLabels.append(str(point.yValue))
            else:
                self.yLabels.append(point.yLabel)

            if point.xLabel == None:
                self.xLabels.append(str(point.xValue))
            else:
                self.xLabels.append(point.xLabel)