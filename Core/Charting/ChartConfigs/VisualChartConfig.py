from Core.Charting.ChartConfigs.GridConfig import GridConfig
from Core.Charting.ChartConfigs.LegendConfig import LegendConfig
from Core.Charting.ChartConfigs.PlotConfig import PlotConfig
from Core.Charting.ChartConfigs.FigureSize import FigureSize

class VisualChartConfig:
    def __init__(self, gridConfig: GridConfig = None, plotConfig: PlotConfig = None, figureSize: FigureSize = None, legendConfig: LegendConfig = None):
        self.gridConfig = gridConfig
        self.plotConfig = plotConfig
        self.figureSize = figureSize
        self.legendConfig = legendConfig