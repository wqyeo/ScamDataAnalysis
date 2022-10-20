import asyncio

from Core.Async.TaskThread import TaskThread
from Core.Util import *

from DataVisualization.Model.DataMergerModel import *
from DataVisualization.View.DataMergerView import *
from DataVisualization.VisualizationViewModel import VisualizationViewModel

MERGE_TASK_NAME = "MERGE_TASK"

class DataMergerViewModel(VisualizationViewModel):
    def __init__(self, appRef) -> None:
        super().__init__(appRef, DataMergerModel(self), MERGED_PLOT_IMAGE_KEY, USER_MESSAGE_KEY, MERGED_PLOT_IMAGES_SELECTOR_KEY)

    def Update(self, event, value):
        if event == START_MERGE_EVENT:
            self._MergeEvent()

        # For animating "Analzying.." message for user.
        if not self._analyzeThread == None:
            if self._analyzeThread.isRunning:
                self._cycle += 1
                if self._cycle >= 9000:
                    self._userMessageCycle += 1
                    if self._userMessageCycle >= 4:
                        self._userMessageCycle = 1
                    self.ShowUserMessage("Merging" + ("." * self._userMessageCycle))

        imageSelection = self._appWindow[MERGED_PLOT_IMAGES_SELECTOR_KEY].get()
        self._UpdateFigure(imageSelection)

    def _MergeEvent(self):

        newThread = TaskThread(MERGE_TASK_NAME)
        if not self.appRef.TryAddTask(newThread):
            self.ShowUserMessage("Already Merging...")
            return None

        self._analyzeThread = newThread

        firstFilePath = self.appRef.window[FIRST_MERGE_FILE_LOCATION_KEY].get()
        secondFilePath = self.appRef.window[SECOND_FILE_LOCATION_KEY].get()

        asyncio.run_coroutine_threadsafe(self.model.MergeData(firstFilePath, secondFilePath, newThread), self.appRef.asyncLoop)
        self.ShowUserMessage("Analyzing.")