import matplotlib.figure
import matplotlib.pyplot as plt
from Core.Util import *

from DataVisualization.Model.DataVisualizationModel import DataVisualizationModel
from DataVisualization.View.DataVisualizationView import *

class DataVisualizationViewModel:
    def __init__(self, appRef) -> None:
        self.appRef = appRef
        self.model = DataVisualizationModel(self)

        self._appWindow = appRef.window
        self._figurePathBindings = {}
        self._lastFigure = ""

    def Update(self, event, value):
        if event == START_ANALYZE_EVENT:
            self._AnalyzeEvent()

        imageSelection = self._appWindow[PLOT_IMAGES_SELECTOR_KEY].get()
        self._UpdateFigure(imageSelection)

    def _AnalyzeEvent(self):
#region Local_Function
        def BindFigurePaths(plotPaths: list) -> None:
            self._figurePathBindings = {}
            for path in plotPaths:
                name = GetFileNameFromPath(path)
                self._figurePathBindings[name.replace("_", " ")] = path
#endregion

        targetFilePath = self.appRef.window[TARGET_FILE_LOCATION_KEY].get()
        figurePaths = self.model.AnalyzeData(targetFilePath)

        if figurePaths != None:
            BindFigurePaths(figurePaths)
            figureNames = list(self._figurePathBindings.keys())
            self._UpdateFigure(figureNames[0], True)
            self._appWindow[PLOT_IMAGES_SELECTOR_KEY].update(values=figureNames, visible=True)

    def _UpdateFigure(self, figName, ignoreLast = False) -> None:
        if figName in self._figurePathBindings:
            if figName != self._lastFigure and not ignoreLast:
                self._lastFigure = figName
                self._appWindow[PLOT_IMAGE_KEY].update(self._figurePathBindings[figName])
            elif ignoreLast:
                self._lastFigure = figName
                self._appWindow[PLOT_IMAGE_KEY].update(self._figurePathBindings[figName])

    def ShowUserMessage(self, message: str) -> None:
        self._appWindow[USER_MESSAGE_KEY].update(message)