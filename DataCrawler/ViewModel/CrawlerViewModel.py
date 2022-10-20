import asyncio

from Core.Async.TaskThread import TaskThread
from DataCrawler.View.CrawlerView import *
from DataCrawler.Model.CrawlerModel import CrawlerModel
from DataCrawler.CrawlViewModel import CrawlViewModel

CRAWL_TASK_THREAD = "SCAM_ALERT_STORIES_CRAWL_TASK"

class CrawlerViewModel(CrawlViewModel):
    def __init__(self, appRef) -> None:
        model = CrawlerModel(self)
        super().__init__(appRef, model, CRAWLER_USER_LOG_KEY, LOADING_BAR_KEY)

    def Update(self, event, value) -> None:
        if event == START_CRAWL_EVENT:
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