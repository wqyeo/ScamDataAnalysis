from Core.Analytics.Analyzer import Analyzer
from Core.Util import *
from Core.Logging.Logger import *
from Core.Logging.LogSeverity import LogSeverity


class DataVisualizationModel:
    def __init__(self, viewModelRef) -> None:
        self.viewModelRef = viewModelRef
        pass

    def AnalyzeData(self, filePath) -> list:
        """
        Tries to analyze data based on the given file path

        ## Output
        List of paths to plot figure. None if invalid analysis. 
        """

        if not IsValidFilePath(filePath):
            Log("Invalid File Path Given", "User gave a possible invalid file path, {}.".format(filePath), LogSeverity.WARNING)
            return None

        dataAnalyzer = Analyzer(filePath, self)

        figurePath = dataAnalyzer.AnalyzeData()
        return figurePath

    def ShowUserMessage(self, message: str) -> None:
        self.viewModelRef.ShowUserMessage(message)