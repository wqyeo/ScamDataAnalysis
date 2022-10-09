import asyncio

import PySimpleGUI as sg

from Core.Async.TaskThread import TaskThread
from DataCrawler.View.DeepCrawlerView import *
from DataCrawler.Model.DeepCrawlerModel import *

DEEP_CRAWL_TASK_NAME = "DETAILED_SCAMALERT_STORIES_CRAWL_TASK"

class DeepCrawlerViewModel:
    def __init__(self, appRef) -> None:
        self.appRef = appRef
        self.model = DeepCrawlerModel(self)
        pass

    def Update(self, event, value) -> None:
        if event == START_CRAWL:
            self.StartCrawl(self.appRef.window) 

    def StartCrawl(self, window) -> None:
        newThread = TaskThread(DEEP_CRAWL_TASK_NAME)
        if not self.appRef.TryAddTask(newThread):
            # TODO: Allow user to cancel crawling?
            self.ShowUserMessage("Already Crawling...")
            return None

        filePath = window[TARGET_CRAWL_DATA_KEY].get()
        
        asyncio.run_coroutine_threadsafe(self.model.CrawlAndSaveData(filePath, newThread), self.appRef.asyncLoop)
        self.ShowUserMessage("Crawling...")

    def ShowUserMessage(self, message) -> None:
        """
        Show a message to the user.
        (Commonly used to show error or log.)
        """
        self.appRef.window[CRAWLER_USER_LOG_KEY].update(message)

    def UpdateLoadingBar(self, percentValue: int) -> None:
        self.appRef.window[LOADING_BAR_KEY].update(percentValue)

    def FreeAppThread(self):
        self.appRef.asyncTaskManager.RemoveIdleTasks()