from Core.Charting.ChartConfigs.PlotConfig import PlotConfig
from Core.Charting.DataCategory import DataCategory
from Core.Charting.Data import Data
from Core.Charting.Charts.LineChart import LineChart
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
        return False

    def _PlotScamAlertStories(self) -> None:
#region Local_Function
        def GenerateConfiguration() -> VisualChartConfig:
            pltConfig = PlotConfig(10)
            return VisualChartConfig(plotConfig= pltConfig)

        def SortDate(date):
            dateStr = date.split(" ")
            year = int(dateStr[2])
            month = MonthStrToInt(dateStr[1])
            day = int(dateStr[0])

            return (year * 12 * 30) + (month * 30) + day
#endregion

        dates = sorted(self.analyzedData["Dates"], key=SortDate)
        dataPoints = Data(DataCategory.DATE)

        for date in dates:
            dataPoints.AppendData(date)

        lineChart = LineChart("Scam Over Time", dataPoints)
        filePath = os.path.join(self.savePath, "dateFig.png")
        PlotChart(lineChart, filePath, GenerateConfiguration())