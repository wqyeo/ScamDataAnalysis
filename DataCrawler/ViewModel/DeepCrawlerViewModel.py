import asyncio

import PySimpleGUI as sg

from Core.Async.TaskThread import TaskThread
from DataCrawler.View.DeepCrawlerView import *

class DeepCrawlerViewModel:
    def __init__(self, appRef) -> None:
        self.appRef = appRef

        # TODO: Model
        self.model = None
        self.currThread = None
        pass

    def Update(self, window) -> None:
        event, value = window.read(timeout=500)
        if event == sg.WINDOW_CLOSED:
            self.appRef.CloseApp()
        elif event == START_CRAWL:
            self.StartCrawl(window) 

    def StartCrawl(self, window) -> None:
        if self.IsCurrTaskRunning():
            return

        filePath = window[TARGET_CRAWL_DATA_KEY].get()
        # TODO: Crawl
        print("deep crawling triggered")

    def ShowUserMessage(self, message) -> None:
        """
        Show a message to the user.
        (Commonly used to show error or log.)
        """
        self.appRef.window[CRAWLER_USER_LOG_KEY].update(message)

    def UpdateLoadingBar(self, percentValue: int) -> None:
        self.appRef.window[LOADING_BAR_KEY].update(percentValue)

    def IsCurrTaskRunning(self) -> bool:
        if self.currThread == None:
            return False
        if self.currThread.isRunning:
            return True
        return True