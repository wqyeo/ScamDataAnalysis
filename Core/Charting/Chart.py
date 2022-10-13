from Core.Charting.ChartConfigs.PlotConfig import PlotConfig
from Core.Charting.ChartConfigs.FigureSize import FigureSize
from Core.Charting.DataCategory import DataCategory
from Core.Charting.Charts.LineChart import LineChart
from Core.Charting.Data import Data
from Core.Charting.Plotter import *

from Core.Util import *
from Core.Logging.Logger import *
from Core.Analytics.DataType import DataType

class Chart:
    def __init__(self, savePath: str, analyzedData: dict, dataType: DataType) -> None:
        """
        **analyzedData**
        All data inside should be sorted from lowest-highest
        """
        self.savePath = savePath
        self.analyzedData = analyzedData
        self.dataType = dataType

    def Plot(self) -> bool:
        CreateToPath(self.savePath)

        if self.dataType == DataType.SCAM_ALERT_STORIES:
            self._PlotScamAlertStories()
            return True
        elif self.dataType == DataType.DETAILED_SCAM_ALERT_STORIES:
            self._PlotDetailedScamAlertStories()
            return True
        return False

    def _PlotScamAlertStories(self) -> None:
        self._PlotScamOverTime()
        self._PlotScamByDates()

    def _PlotDetailedScamAlertStories(self) -> None:
        self._PlotScamOverTime()
        self._PlotScamByDates()
        self._PlotScamTypes()

    def _PlotScamTypes(self):
        scamTypes = self.analyzedData["ScamTypes"]
        dataPoints = Data(DataCategory.COUNTABLES)

        for scamType in scamTypes:
            dataPoints.AppendData(scamType)

        pieChart = PieChart("Scam Types Occurance", dataPoints)
        filePath = os.path.join(self.savePath, "Scam_Type_Occurance.png")
        PlotChart(pieChart, filePath, None)

    def _PlotScamOverTime(self):
#region Local_Function
        def GenerateConfiguration(data: Data) -> VisualChartConfig:
            intervals = -1
            if data.Size() > 10:
                intervals = data.Size() // 10

            figSize = FigureSize(6, 6)
            pltConfig = PlotConfig(intervals, intervals, xRotation="vertical")
            return VisualChartConfig(plotConfig= pltConfig, figureSize=figSize)
#endregion

        dates = sorted(self.analyzedData["Dates"], key=Chart._SortDate)
        dataPoints = Data(DataCategory.DATE_OVER_TIME)

        for date in dates:
            dataPoints.AppendData(date)

        lineChart = LineChart("Scam Over Time", dataPoints)
        filePath = os.path.join(self.savePath, "Scam_Over_Time.png")
        PlotChart(lineChart, filePath, GenerateConfiguration(dataPoints))

    def _PlotScamByDates(self):
#region Local_Function
        def GenerateConfiguration(data: Data) -> VisualChartConfig:
            intervals = -1
            if data.Size() > 10:
                intervals = data.Size() // 10

            figSize = FigureSize(6, 6)
            pltConfig = PlotConfig(intervals, xRotation="vertical")
            return VisualChartConfig(plotConfig= pltConfig, figureSize=figSize)
#endregion

        dates = sorted(self.analyzedData["Dates"], key=Chart._SortDate)
        dataPoints = Data(DataCategory.DATE)

        for date in dates:
            dataPoints.AppendData(date)

        lineChart = LineChart("Scam By Date", dataPoints)
        filePath = os.path.join(self.savePath, "Scam_By_Date.png")
        PlotChart(lineChart, filePath, GenerateConfiguration(dataPoints))

    def _SortDate(date):
        dateStr = date.split(" ")
        year = int(dateStr[2])
        month = MonthStrToInt(dateStr[1])
        day = int(dateStr[0])

        return (year * 12 * 30) + (month * 30) + day