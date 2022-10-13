from model.chart_configs.plot_config import PlotConfig

class BarPlotConfig(PlotConfig):
    def __init__(self, align: str = 'center', width : float = 0.4):
        self.align = align
        self.width = width
