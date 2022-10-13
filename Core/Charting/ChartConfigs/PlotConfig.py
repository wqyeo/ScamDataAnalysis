class PlotConfig:
    def __init__(self, xTickIntervals: int = -1, yTickIntervals: int = -1, xRotation = "horizontal", yRotation = "horizontal"):
        self.xTickIntervals = xTickIntervals
        self.yTickIntervals = yTickIntervals

        self.xRotation = xRotation
        self.yRotation = yRotation