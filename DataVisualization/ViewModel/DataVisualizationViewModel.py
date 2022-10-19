import asyncio

from Core.Async.TaskThread import TaskThread
from Core.Util import *

from DataVisualization.Model.DataVisualizationModel import DataVisualizationModel
from DataVisualization.View.DataVisualizationView import *
from DataVisualization.VisualizationViewModel import VisualizationViewModel

ANALYZE_TASK_NAME = "ANALYZE_TASK"

class DataVisualizationViewModel(VisualizationViewModel):
    def __init__(self, appRef) -> None:
        super().__init__(appRef, DataVisualizationModel(self), PLOT_IMAGE_KEY, USER_MESSAGE_KEY, PLOT_IMAGES_SELECTOR_KEY)

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