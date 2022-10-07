import asyncio

import PySimpleGUI as sg

from Core.Async.TaskThread import TaskThread
from DataCrawler.View.DeepCrawlerView import *
from DataCrawler.Model.DeepCrawlerModel import *

class DeepCrawlerViewModel:
    def __init__(self, appRef) -> None:
        self.appRef = appRef

        # TODO: Model
        self.model = DeepCrawlerModel(self)
        self.currThread = None
        pass

    def Update(self, window) -> None:
        event, value = window.read()
        if event == sg.WINDOW_CLOSED:
            self.appRef.CloseApp()
        elif event == START_CRAWL:
            self.StartCrawl(window) 

    def StartCrawl(self, window) -> None:
        if self.IsCurrTaskRunning():
            return

        filePath = window[TARGET_CRAWL_DATA_KEY].get()
        
        self.currThread = TaskThread("Deep Crawl and Save")
        asyncio.run_coroutine_threadsafe(self.model.CrawlAndSaveData(filePath, self.currThread), self.appRef.asyncLoop)
        print("Deep Crawl Triggered")

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