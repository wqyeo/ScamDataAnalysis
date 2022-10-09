import asyncio

import PySimpleGUI as sg

from Core.Async.TaskThread import TaskThread
from DataCrawler.View.CrawlerView import *
from DataCrawler.Model.CrawlerModel import CrawlerModel

CRAWL_TASK_THREAD = "SCAM_ALERT_STORIES_CRAWL_TASK"

class CrawlerViewModel:
    def __init__(self, appRef) -> None:
        self.appRef = appRef
        self.model = CrawlerModel(self)

    def Update(self, event, value) -> None:
        if event == START_CRAWL:
            self.StartCrawl(self.appRef.window)

    def StartCrawl(self, window) -> None:
        newThread = TaskThread(CRAWL_TASK_THREAD)

        if not self.appRef.TryAddTask(newThread):
            # TODO: Allow user to cancel crawling?
            self.ShowUserMessage("Already Crawling...")
            return

        filePath = window[SAVE_FOLDER_KEY].get()
        recursiveNum = window[RECURSIVE_CRAWL_TIMES_KEY].get()
        targetSite = window[TARGET_CRAWL_SITE_KEY].get()
        asyncio.run_coroutine_threadsafe(self.model.CrawlAndSaveData(filePath, recursiveNum, targetSite, taskThread=newThread), self.appRef.asyncLoop)

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