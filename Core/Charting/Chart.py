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
        self.analyzedData = sorted(analyzedData, key=Chart._GetRawDateValue)
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
        self._PlotScamOverTime("Scam_Over_Time")
        #self._PlotScamByDates("Scam_By_Date")

        for year in range(2018, 2023):
            def YearFilter(data):
                return Chart._GetRawDateValue(data) < (year * 12 * 30) or Chart._GetRawDateValue(data) > ((year + 1) * 12 * 30)

            self._PlotScamOverTime("Scam_Over_Time_" + str(year), YearFilter)
            #self._PlotScamByDates("Scam_By_Date_" + str(year), YearFilter)

    def _PlotDetailedScamAlertStories(self) -> None:
        figSize = FigureSize(6, 6)
        pieChartConfig = VisualChartConfig(figureSize=figSize)

        self._PlotScamOverTime("Scam_Over_Time")
        #self._PlotScamByDates("Scam_By_Date")
        self._PlotCountablePieChart("ScamTypes", "Scam_Types_Occurance", pieChartConfig)
        self._PlotCountablePieChart("PlatformTypes", "Scam_Target_Platforms", pieChartConfig)

        legendConfig = LegendConfig(True)
        pieChartConfig.legendConfig = legendConfig

        for year in range(2019, 2022):
            def YearFilter(data):
                return Chart._GetRawDateValue(data) < (year * 12 * 30) or Chart._GetRawDateValue(data) > ((year + 1) * 12 * 30)

            self._PlotScamOverTime("Scam_Over_Time_" + str(year), YearFilter)
            #self._PlotScamByDates("Scam_By_Date_" + str(year), YearFilter)
            self._PlotCountablePieChart("ScamTypes", "Scam_Types_Occurance_" + str(year), pieChartConfig, YearFilter)
            self._PlotCountablePieChart("PlatformTypes", "Scam_Target_Platforms_" + str(year), pieChartConfig, YearFilter)

    def _PlotCountablePieChart(self, key: str, fileName: str, chartConfig: VisualChartConfig = None, filter = None):
        dataPoints = Data(DataCategory.COUNTABLES)

        for data in self.analyzedData:
            if filter != None:
                if filter(data):
                    continue
            toCount = data[key]
            if toCount != None:
                dataPoints.AppendData(toCount)

        pieChart = PieChart(fileName.replace("_", " "), dataPoints)
        filePath = os.path.join(self.savePath, fileName + ".png")
        PlotChart(pieChart, filePath, chartConfig)

    def _PlotScamOverTime(self, fileName: str, filter = None):
#region Local_Function
        def GenerateConfiguration(data: Data) -> VisualChartConfig:
            intervals = -1
            if data.Size() > 10:
                intervals = data.Size() // 10

            figSize = FigureSize(6, 6)
            pltConfig = PlotConfig(intervals, intervals, xRotation="vertical")
            return VisualChartConfig(plotConfig= pltConfig, figureSize=figSize)
#endregion

        dataPoints = Data(DataCategory.DATE_OVER_TIME)

        for data in self.analyzedData:
            if filter != None:
                if filter(data):
                    continue
            date = data["Dates"]
            if date != None:
                dataPoints.AppendData(date)

        lineChart = LineChart(fileName.replace("_", " "), dataPoints)
        filePath = os.path.join(self.savePath, fileName + ".png")
        PlotChart(lineChart, filePath, GenerateConfiguration(dataPoints))

    def _PlotScamByDates(self, fileName: str, filter = None):
#region Local_Function
        def GenerateConfiguration(data: Data) -> VisualChartConfig:
            intervals = -1
            if data.Size() > 10:
                intervals = data.Size() // 10

            figSize = FigureSize(6, 6)
            pltConfig = PlotConfig(intervals, xRotation="vertical")
            return VisualChartConfig(plotConfig= pltConfig, figureSize=figSize)
#endregion

        dataPoints = Data(DataCategory.DATE)

        for data in self.analyzedData:
            if filter != None:
                if filter(data):
                    continue
            date = data["Dates"]
            if date != None:
                dataPoints.AppendData(date)


        lineChart = LineChart(fileName.replace("_", " "), dataPoints)
        filePath = os.path.join(self.savePath, fileName + ".png")
        PlotChart(lineChart, filePath, GenerateConfiguration(dataPoints))

    def _GetRawDateValue(data):
        dateStr = data["Dates"].split(" ")
        year = int(dateStr[2])
        month = MonthStrToInt(dateStr[1])
        day = int(dateStr[0])

        return (year * 12 * 30) + (month * 30) + day