import PySimpleGUI as sg

from DataCrawler.View.CrawlerView import *
from DataCrawler.View.DeepCrawlerView import *
from DataCrawler.ViewModel.CrawlerViewModel import CrawlerViewModel
from DataCrawler.ViewModel.DeepCrawlerViewModel import DeepCrawlerViewModel

from WindowApp import WindowApp

class DataCrawlerApp(WindowApp):
    def __init__(self, mainAsyncLoop) -> None:
        window = sg.Window(title = "Data Crawler", layout= DataCrawlerApp._CreateLayout(), margins=(0, 0))
        viewModels = [
            CrawlerViewModel(self),
            DeepCrawlerViewModel(self) 
        ]
        super().__init__(mainAsyncLoop, window, viewModels)

    def _OnAppCloseEvent(self) -> bool:
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
            return True
        return False

    def _CreateLayout():
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