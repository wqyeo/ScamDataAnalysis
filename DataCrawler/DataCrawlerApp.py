import PySimpleGUI as sg

from DataCrawler.View.CrawlerView import *
from DataCrawler.View.DeepCrawlerView import *
from DataCrawler.ViewModel.CrawlerViewModel import CrawlerViewModel

class DataCrawlerApp:
    def __init__(self, mainAsyncLoop) -> None:
        self.window = sg.Window(title = "Data Crawler", layout= APP_VIEW, margins=(0, 0))
        self.isOpen = True
        self.currViewModel = CrawlerViewModel(self)
        self.asyncLoop = mainAsyncLoop
        pass

    def Update(self) -> None:
        self.currViewModel.Update(self.window)

    def CloseApp(self):
        self.isOpen = False

# NOTE: App View
APP_TAB_GROUP = sg.TabGroup(
    [[
        sg.Tab("Site", CreateCrawlerViewLayout()),
        sg.Tab("Deep", CreateDeepCrawlerViewLayout())
    ]]
)

APP_VIEW = [
    [APP_TAB_GROUP]
]
