import asyncio

from Core.Async.TaskThread import TaskThread
from DataCrawler.CrawlViewModel import CrawlViewModel
from DataCrawler.View.DeepCrawlerView import *
from DataCrawler.Model.DeepCrawlerModel import *

DEEP_CRAWL_TASK_NAME = "DETAILED_SCAMALERT_STORIES_CRAWL_TASK"

class DeepCrawlerViewModel(CrawlViewModel):
    def __init__(self, appRef) -> None:
        model = DeepCrawlerModel(self)
        super().__init__(appRef, model, CRAWLER_USER_LOG_KEY, LOADING_BAR_KEY)

    def Update(self, event, value) -> None:
        if event == START_CRAWL_EVENT:
            self.StartCrawl(self.appRef.window) 

    def StartCrawl(self, window) -> None:
        newThread = TaskThread(DEEP_CRAWL_TASK_NAME)
        if not self.appRef.TryAddTask(newThread):
            self.ShowUserMessage("Already Crawling...")
            return None

        filePath = window[TARGET_CRAWL_DATA_KEY].get()
        
        asyncio.run_coroutine_threadsafe(self.model.CrawlAndSaveData(filePath, newThread), self.appRef.asyncLoop)
        self.ShowUserMessage("Crawling...")