from Core.Charting.Data import Data
from Core.Charting.Charts.VisualChart import VisualChart

class PieChart(VisualChart):
    def __init__(self, title, data: list, othersCutOff: int = 10, showPercentage: bool = True):
        """
        A Pie Chart

        Parameters
        ------------------------
        **others_cut_off**
        Anything below this value will be categorised into 'others' section instead.
        """
        self.values = []
        self.labels = []
        self.othersCutOff = othersCutOff
        self._nonPercentLabel = []
        self._totalValue = 0.0
        self._UnpackData(data, showPercentage)

        if showPercentage:
            self._EvaluatePercentage()
        super().__init__(title+ " (" + str(data.dataSize) + ")")

    def _UnpackData(self, data: Data, showPercentage: bool):
        othersCount = 0
        for point in data.points:
            if point.xValue < self.othersCutOff:
                othersCount += point.xValue
            else:
                self.values.append(point.xValue)
                self.labels.append(point.yLabel)
                if showPercentage:
                    self._nonPercentLabel.append(point.yLabel)
            self._totalValue += point.xValue

        if othersCount > 0:
            self.values.append(othersCount)
            self.labels.append("Others")

    def _EvaluatePercentage(self):
        for i in range(len(self.labels)):
            val = self.values[i]
            percent = (val / self._totalValue) * 100.0
            self.labels[i] += " ({:.1f}%)".format(percent)

    def GetNonPercentageLabels(self) -> list:
        if len(self._nonPercentLabel) >= 1:
            return self._nonPercentLabel
        else:
            return self.labels