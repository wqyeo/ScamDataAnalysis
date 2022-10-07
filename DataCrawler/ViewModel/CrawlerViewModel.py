import asyncio

import PySimpleGUI as sg

from Core.Async.TaskThread import TaskThread
from DataCrawler.View.CrawlerView import *
from DataCrawler.Model.CrawlerModel import CrawlerModel

class CrawlerViewModel:
    def __init__(self, appRef) -> None:
        self.appRef = appRef
        self.model = CrawlerModel(self)
        self.currThread = None
        pass

    def Update(self, event, value) -> None:
        if event == sg.WINDOW_CLOSED:
            self.appRef.CloseApp()
        elif event == START_CRAWL:
            self.StartCrawl(self.appRef.window)

    def StartCrawl(self, window) -> None:
        if self.IsCurrTaskRunning():
            return

        filePath = window[SAVE_FOLDER_KEY].get()
        recursiveNum = window[RECURSIVE_CRAWL_TIMES_KEY].get()

        self.currThread = TaskThread("Crawl and Save")
        targetSite = window[TARGET_CRAWL_SITE_KEY].get()
        asyncio.run_coroutine_threadsafe(self.model.CrawlAndSaveData(filePath, recursiveNum, targetSite, taskThread=self.currThread), self.appRef.asyncLoop)

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