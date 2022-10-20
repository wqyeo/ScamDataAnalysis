import PySimpleGUI as sg

from DataVisualization.View.DataVisualizationView import *
from DataVisualization.View.DataMergerView import *
from DataVisualization.ViewModel.DataMergerViewModel import DataMergerViewModel
from DataVisualization.ViewModel.DataVisualizationViewModel import *

from WindowApp import WindowApp


class DataVisualizationApp(WindowApp):
    def __init__(self, mainAsyncLoop) -> None:
        window = sg.Window(title="Data Visualization", layout=DataVisualizationApp._CreateLayout(),
                                margins=(0, 0))
        self.window = window
        viewModels = [
            DataVisualizationViewModel(self),
            DataMergerViewModel(self)
        ]

        super().__init__(mainAsyncLoop, window, viewModels)

    def _OnAppCloseEvent(self) -> bool:
        choice = "Yes"
        self.asyncTaskManager.RemoveIdleTasks()
        if len(self.asyncTaskManager.currentTasks) > 0:
            # Create Popup to notify user that a crawling thread is still active.
            # User can choose to cancel it.
            choice, _ = sg.Window('Cancel Analysis',
                                    [[sg.T('Analyzer is still actively analyzing, cancel analysis?')],
                                    [sg.Yes(s=10), sg.No(s=10)]], disable_close=True).read(close=True)

        # Default if no thread/task.
        # or when user choose to cancel.
        if choice == "Yes":
            self.asyncTaskManager.EndAllTask()
            self.CloseApp()
            return True
        return False

    def _CreateLayout():
        # NOTE: App View
        APP_TAB_GROUP = sg.TabGroup(
            [[
                sg.Tab("Analyze", CreateVisualizationViewLayout()),
                sg.Tab("Merger", CreateMergerViewLayout())
            ]]
        )

        return [
            [APP_TAB_GROUP]
        ]