from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io

from Core.Analytics.Analyzer import Analyzer
from Core.Util import *
from Core.Logging.Logger import *
from Core.Logging.LogSeverity import LogSeverity


class DataVisualizationModel:
    def __init__(self, viewModelRef) -> None:
        self.viewModelRef = viewModelRef
        pass

    def AnalyzeData(self, filePath) -> str:
        """
        Tries to analyze data based on the given file path

        ## Output
        Path to plot figure. None if invalid analysis. 
        """

        if not IsValidFilePath(filePath):
            Log("Invalid File Path Given", "User gave a possible invalid file path, {}.".format(filePath), LogSeverity.WARNING)
            return None

        dataAnalyzer = Analyzer(filePath)

        # TODO: Show figures
        if dataAnalyzer.AnalyzeData():
           return None
        return None

    def draw_figure(self, figure):
        plt.close('all')  # erases previously drawn plots
        canv = FigureCanvasAgg(figure)
        buf = io.BytesIO()
        canv.print_figure(buf, format='png')
        if buf is None:
            return None
        buf.seek(0)
        self.update(data=buf.read())
        return canv
