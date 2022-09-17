import PySimpleGUI as sg

from DataCrawler.View.CrawlerView import *

class DataCrawlerApp:
    def __init__(self) -> None:
        self.window = sg.Window(title = "Data Crawler", layout= CreateCrawlerViewLayout(), margins=(50, 20))
        self.isOpen = True
        pass

    def Update(self) -> None:
        event, value = self.window.read()
        if event == sg.WINDOW_CLOSED:
            self.isOpen = False
        elif event == START_CRAWL:
            print("User requested to crawl")