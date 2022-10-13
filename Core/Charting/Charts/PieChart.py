from Core.Charting.Data import Data
from Core.Charting.Charts.VisualChart import VisualChart

class PieChart(VisualChart):
    def __init__(self, title, data: list, othersCutOff: int = 3):
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

        self._UnpackData(data)
        super().__init__(title)

    def _UnpackData(self, data: Data):
        othersCount = 0
        for point in data.points:
            if point.xValue < self.othersCutOff:
                othersCount += point.xValue
            else:
                self.values.append(point.xValue)
                self.labels.append(point.yLabel)

        if othersCount > 0:
            self.values.append(othersCount)
            self.labels.append("Others")