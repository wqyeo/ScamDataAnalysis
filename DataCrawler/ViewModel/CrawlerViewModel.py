import PySimpleGUI as sg

from DataCrawler.View.CrawlerView import *
from DataCrawler.Model.CrawlerModel import CrawlerModel

class CrawlerViewModel:
    def __init__(self, appRef) -> None:
        self.appRef = appRef
        self.model = CrawlerModel(self)
        pass

    def Update(self, window) -> None:
        event, value = window.read()
        if event == sg.WINDOW_CLOSED:
            self.appRef.CloseApp()
        elif event == START_CRAWL:
            self.StartCrawl(window)

    def StartCrawl(self, window) -> None:
        filePath = window[SAVE_FOLDER_KEY].get()
        recursiveNum = window[RECURSIVE_CRAWL_TIMES_KEY].get()

        self.model.CrawlAndSaveData(filePath, recursiveNum)

    def ShowUserMessage(self, message) -> None:
        """
        Show a message to the user.
        (Commonly used to show error or log.)
        """
        self.appRef.window[CRAWLER_USER_LOG_KEY].update(message)