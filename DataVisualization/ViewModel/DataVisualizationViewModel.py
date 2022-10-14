import asyncio

from Core.Async.TaskThread import TaskThread
from Core.Util import *

from DataVisualization.Model.DataVisualizationModel import DataVisualizationModel
from DataVisualization.View.DataVisualizationView import *

ANALYZE_TASK_NAME = "ANALYZE_TASK"

class DataVisualizationViewModel:
    def __init__(self, appRef) -> None:
        self.appRef = appRef
        self.model = DataVisualizationModel(self)

        self._appWindow = appRef.window
        self._figurePathBindings = {}
        self._lastFigure = ""

        # For 'animating' a loading message
        self._analyzeThread = None
        self._userMessageCycle = 1
        self._cycle = 0

    def Update(self, event, value):
        if event == START_ANALYZE_EVENT:
            self._AnalyzeEvent()

        # For animating "Analzying.." message for user.
        if not self._analyzeThread == None:
            if self._analyzeThread.isRunning:
                self._cycle += 1
                if self._cycle >= 9000:
                    self._userMessageCycle += 1
                    if self._userMessageCycle >= 4:
                        self._userMessageCycle = 1
                    self.ShowUserMessage("Analyzing" + ("." * self._userMessageCycle))

        imageSelection = self._appWindow[PLOT_IMAGES_SELECTOR_KEY].get()
        self._UpdateFigure(imageSelection)

    def _AnalyzeEvent(self):

        newThread = TaskThread(ANALYZE_TASK_NAME)
        if not self.appRef.TryAddTask(newThread):
            self.ShowUserMessage("Already Analyzing...")
            return None

        self._analyzeThread = newThread

        targetFilePath = self.appRef.window[TARGET_FILE_LOCATION_KEY].get()

        asyncio.run_coroutine_threadsafe(self.model.AnalyzeData(targetFilePath, newThread), self.appRef.asyncLoop)
        self.ShowUserMessage("Analyzing.")

    def SetFigurePaths(self, figurePaths: str) -> None:
#region Local_Function
        def BindFigurePaths(plotPaths: list) -> None:
            self._figurePathBindings = {}
            for path in plotPaths:
                name = GetFileNameFromPath(path)
                self._figurePathBindings[name.replace("_", " ")] = path
#endregion

        if figurePaths != None:
            BindFigurePaths(figurePaths)
            figureNames = list(self._figurePathBindings.keys())
            self._UpdateFigure(figureNames[0], True)
            self._appWindow[PLOT_IMAGES_SELECTOR_KEY].update(values=figureNames, visible=True)
            self.ShowUserMessage("Analyzed!")
        else:
            self.ShowUserMessage("Analyze failed or cancelled.")

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

    def FreeAppThread(self):
        self.appRef.asyncTaskManager.RemoveIdleTasks()