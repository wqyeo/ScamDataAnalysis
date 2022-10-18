from Core.Async.TaskThread import TaskThread
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
    def __init__(self, savePath: str, analyzedData, dataType: DataType, thread: TaskThread = None) -> None:
        """
        **analyzedData**
        All data inside should be sorted from lowest-highest
        """
        self.savePath = savePath
        self.analyzedData = sorted(analyzedData, key=Chart._GetRawDateValue)
        self.dataType = dataType
        self._thread = thread

    def Plot(self) -> bool:
        CreateToPath(self.savePath)

        if self.dataType == DataType.SCAM_ALERT_STORIES or self.dataType == DataType.SCAM_ALERT_NEWS:
            self._PlotDates()
            return True
        elif self.dataType == DataType.DETAILED_SCAM_ALERT_STORIES or self.dataType == DataType.DETAILED_SCAM_ALERT_NEWS or DataType.MERGED_DATA:
            self._PlotDetailedData()
            return True
        return False

    def _PlotDates(self) -> None:
        self._PlotScamOverTime("Scam_Over_Time")
        #self._PlotScamByDates("Scam_By_Date")

        for year in range(2019, 2023):
            def YearFilter(data):
                return Chart._GetRawDateValue(data) < (year * 12 * 30) or Chart._GetRawDateValue(data) > ((year + 1) * 12 * 30)

            self._PlotScamOverTime("Scam_Over_Time_" + str(year), YearFilter)
            #self._PlotScamByDates("Scam_By_Date_" + str(year), YearFilter)

    def _PlotDetailedData(self) -> None:
        figSize = FigureSize(6, 6)
        legendConfig = LegendConfig(True)
        pieChartConfig = VisualChartConfig(figureSize=figSize, legendConfig=legendConfig)

        self._PlotScamOverTime("Scam_Over_Time", filter= lambda d: Chart._GetRawDateValue(d) < (2019 * 12 * 30))
        #self._PlotScamByDates("Scam_By_Date")
        self._PlotCountablePieChart("ScamTypes", "Scam_Types_Occurance", pieChartConfig, showLabel=False)
        self._PlotCountablePieChart("PlatformTypes", "Scam_Target_Platforms", pieChartConfig, showLabel=False)

        for year in range(2018, 2023):
            def YearFilter(data):
                return Chart._GetRawDateValue(data) < (year * 12 * 30) or Chart._GetRawDateValue(data) > ((year + 1) * 12 * 30)

            self._PlotScamOverTime("Scam_Over_Time_" + str(year), YearFilter)
            #self._PlotScamByDates("Scam_By_Date_" + str(year), YearFilter)
            self._PlotCountablePieChart("ScamTypes", "Scam_Types_Occurance_" + str(year), pieChartConfig, YearFilter)
            self._PlotCountablePieChart("PlatformTypes", "Scam_Target_Platforms_" + str(year), pieChartConfig, YearFilter)

    def _PlotCountablePieChart(self, key: str, fileName: str, chartConfig: VisualChartConfig = None, filter = None, showLabel: bool = True):
        """
        Plot down a Pie Chart based on countable data.

        ## Input
        **key**
        The key to use to access the data.

        **fileName**
        Output file name.

        **chartConfig** (Optional)
        Configurations for the shown chart.

        **filter** (Optional)
        A bool-function that gets function passed through it. Return True if you want the passed data to be ignored in the plotting.

        **showLabel** (Optional)
        True to show label in this pie chart.
        """
        dataPoints = Data(DataCategory.COUNTABLES)

        for data in self.analyzedData:
            # End thread if user asked to end
            if self._thread != None:
                if self._thread.isRunning == False:
                    return None

            if filter != None:
                if filter(data):
                    continue

            toCount = None
            if key in data:
                toCount = data[key]
            if toCount != None:
                dataPoints.AppendData(toCount)

        if dataPoints.Size() == 0:
            return None

        pieChart = PieChart(fileName.replace("_", " "), dataPoints, showLabels=showLabel)
        filePath = os.path.join(self.savePath, fileName + ".png")
        PlotChart(pieChart, filePath, chartConfig)

    def _PlotScamOverTime(self, fileName: str, filter = None):
        """
        Plot down a Line Chart based on scams over time.

        ## Input
        **fileName**
        Output file name.

        **filter** (Optional)
        A bool-function that gets function passed through it. Return True if you want the passed data to be ignored in the plotting.
        """
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
            # End thread if user asked to end
            if self._thread != None:
                if self._thread.isRunning == False:
                    return None

            if filter != None:
                if filter(data):
                    continue

            date = None
            if "Dates" in data:
                date = data["Dates"]
            if date != None:
                dataPoints.AppendData(date)

        if dataPoints.Size() == 0:
            return None

        lineChart = LineChart(fileName.replace("_", " "), dataPoints)
        filePath = os.path.join(self.savePath, fileName + ".png")
        PlotChart(lineChart, filePath, GenerateConfiguration(dataPoints))

    def _PlotScamByDates(self, fileName: str, filter = None):
        """
        Plot down a Line Chart based on scam by dates.

        ## Input
        **fileName**
        Output file name.

        **filter** (Optional)
        A bool-function that gets function passed through it. Return True if you want the passed data to be ignored in the plotting.
        """
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
            # End thread if user asked to end
            if self._thread != None:
                if self._thread.isRunning == False:
                    return None

            if filter != None:
                if filter(data):
                    continue

            date = None
            if "Dates" in data:
                date = data["Dates"]
            if date != None:
                dataPoints.AppendData(date)

        if dataPoints.Size() == 0:
            return None

        lineChart = LineChart(fileName.replace("_", " "), dataPoints)
        filePath = os.path.join(self.savePath, fileName + ".png")
        PlotChart(lineChart, filePath, GenerateConfiguration(dataPoints))

    def _GetRawDateValue(data):
        dateStr = data["Dates"].split(" ")

        year = int(dateStr[2])
        month = MonthStrToInt(dateStr[1])
        day = int(dateStr[0])
        return (year * 12 * 30) + (month * 30) + day