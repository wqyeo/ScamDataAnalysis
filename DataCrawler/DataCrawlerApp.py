import PySimpleGUI as sg

from DataCrawler.View.CrawlerView import *
from DataCrawler.ViewModel.CrawlerViewModel import CrawlerViewModel

class DataCrawlerApp:
    def __init__(self) -> None:
        self.window = sg.Window(title = "Data Crawler", layout= CreateCrawlerViewLayout(), margins=(50, 20))
        self.isOpen = True
        self.currViewModel = CrawlerViewModel(self)
        pass

    def Update(self) -> None:
        self.currViewModel.Update(self.window)

    def CloseApp(self):
        self.isOpen = False