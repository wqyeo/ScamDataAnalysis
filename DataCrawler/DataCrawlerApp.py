import PySimpleGUI as sg
from Core.Async.AppTaskManager import AppTaskManager
from Core.Async.TaskThread import TaskThread

from DataCrawler.View.CrawlerView import *
from DataCrawler.View.DeepCrawlerView import *
from DataCrawler.ViewModel.CrawlerViewModel import CrawlerViewModel
from DataCrawler.ViewModel.DeepCrawlerViewModel import DeepCrawlerViewModel

class DataCrawlerApp:
    def __init__(self, mainAsyncLoop) -> None:
        self.window = sg.Window(title = "Data Crawler", layout= DataCrawlerApp.CreateLayout(), margins=(0, 0))
        self.isOpen = True
        self.viewModels = [
            CrawlerViewModel(self),
            DeepCrawlerViewModel(self) 
        ]
        self.asyncLoop = mainAsyncLoop
        self.asyncTaskManager = AppTaskManager(self)

    def Update(self) -> None:
        event, value = self.window.read()

        if event == sg.WINDOW_CLOSED:
            # TODO: Warn if any of the thread are still active.
            self.appRef.CloseApp()
            return
        # TODO: See if it possible to update the respective view-model
        # based on the current viewed Tab.
        for viewModel in self.viewModels:
            viewModel.Update(event, value)

    def CloseApp(self):
        self.isOpen = False

    def CreateLayout():
        # NOTE: App View
        APP_TAB_GROUP = sg.TabGroup(
            [[
                sg.Tab("Site", CreateCrawlerViewLayout()),
                sg.Tab("Deep", CreateDeepCrawlerViewLayout())
            ]]
        )

        return [
            [APP_TAB_GROUP]
        ]

    def TryAddTask(self, task: TaskThread) -> bool:
        """
        Try to add a task to the app's async task pool.

        Return false if the task already exists.
        """
        if self.asyncTaskManager.TaskExists(task):
            return False
        self.asyncTaskManager.AddTask(task)
        return True
