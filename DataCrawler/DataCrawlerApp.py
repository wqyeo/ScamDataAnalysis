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
        event, value = self.window.read(timeout=10)

        if event == sg.WINDOW_CLOSED:
            choice = "Yes"
            self.asyncTaskManager.RemoveIdleTasks()
            if len(self.asyncTaskManager.currentTasks) > 0:
                # Create Popup to notify user that a crawling thread is still active.
                # User can choose to cancel it.
                choice, _ = sg.Window('Cancel Crawling', [[sg.T('Crawler is still actively crawling, cancel crawling?')], [sg.Yes(s=10), sg.No(s=10)]], disable_close=True).read(close=True)

            # Default if no thread/task.
            # or when user choose to cancel.
            if choice == "Yes":
                self.asyncTaskManager.EndAllTask()
                self.CloseApp()
                return None
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
