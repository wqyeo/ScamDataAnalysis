from Core.Charting.Charts.VisualChart import VisualChart

class BarChart(VisualChart):
    def __init__(self, title, data: list):
        super().__init__(title)