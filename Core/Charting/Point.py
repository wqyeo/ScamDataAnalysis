class Point:
    """
    Represents a X-Y point in the chart
    """
    def __init__(self, xValue: int, yValue: int, xLabel = None, yLabel = None):
        self.xValue = xValue
        self.xLabel = xLabel
        self.yValue = yValue
        self.yLabel = yLabel

    # for sorted() func
    def __lt__(self, other):
        return self.value < other.value