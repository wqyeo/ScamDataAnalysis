import linecache
from re import T
import matplotlib.pyplot as plt

from Core.Charting.Charts.VisualChart import VisualChart
from Core.Charting.Charts.LineChart import LineChart
from Core.Logging.LogSeverity import LogSeverity
from Core.Logging.Logger import Log

from Core.Charting.ChartConfigs.VisualChartConfig import VisualChartConfig
from Core.Charting.ChartConfigs.GridConfig import GridConfig

def PlotChart(visualChart: VisualChart,  outputPath: str, chartConfig: VisualChartConfig = None) -> None:
    plt.clf()
    plt.cla()
    plt.close()
    plt.rcParams["figure.figsize"]
    if not chartConfig == None:
        if not chartConfig.figureSize == None:
            plt.figure(figsize=(chartConfig.figureSize.xSize, chartConfig.figureSize.ySize))

    if isinstance(visualChart, LineChart):
        _PrintLineChart(visualChart, outputPath, chartConfig)
    else:
        Log("Unknown Visual Chart Type", "Unknown Visual Chart Type given to ouput to {}".format(outputPath), LogSeverity.WARNING)


def _PrintLineChart(lineChart: LineChart, outputPath: str, chartConfig: VisualChartConfig) -> None:
#region Local_Functions
    def SetPlotGrid():
        nonlocal chartConfig
        gridConfig = GridConfig()
        if not chartConfig == None:
            if not chartConfig.gridConfig == None:
                gridConfig = chartConfig.gridConfig
        plt.grid(axis = gridConfig.GetTargetAxis(), linestyle = gridConfig.linestyle, linewidth = gridConfig.linewidth, which = gridConfig.GetTargetGrid())

    def SetChartTicks():
        nonlocal chartConfig
        ax = plt.gca()
        useDefaultX = True
        useDefaultY = True

        xRotation = "horizontal"
        yRotation = "horizontal"
        if not chartConfig == None:
            if not chartConfig.plotConfig == None:
                xIntervals = chartConfig.plotConfig.xTickIntervals
                yIntervals = chartConfig.plotConfig.yTickIntervals

                xRotation = chartConfig.plotConfig.xRotation
                yRotation = chartConfig.plotConfig.yRotation
                if xIntervals >= 1:
                    ax.set_xticks(lineChart.xValues[::xIntervals])
                    ax.set_xticklabels(lineChart.xLabels[::xIntervals], rotation=xRotation)
                    useDefaultX = False
                if yIntervals >= 1:
                    ax.set_yticks(lineChart.yValues[::yIntervals])
                    ax.set_yticklabels(lineChart.yLabels[::yIntervals], rotation=yRotation)
                    useDefaultY = False

        if useDefaultX:
            ax.set_xticks(lineChart.xValues)
            ax.set_xticklabels(lineChart.xLabels, rotation=xRotation)
        if useDefaultY:
            ax.set_yticks(lineChart.yValues)
            ax.set_yticklabels(lineChart.yLabels, rotation=yRotation)
#endregion

    plt.plot(lineChart.xValues, lineChart.yValues)
    SetPlotGrid()
    plt.title(lineChart.title)
    SetChartTicks()

    plt.tight_layout()
    plt.savefig(outputPath)