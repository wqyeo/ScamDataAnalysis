import asyncio
import os
import json

from Core.Logging.Logger import *
from Core.Crawler import Crawler
from Core.Database import Database

class DeepCrawlerModel:
    def __init__(self, viewModelRef) -> None:
        self.viewModelRef = viewModelRef
        pass

    @asyncio.coroutine
    def CrawlAndSaveData(self, targetDataPath: str, taskThread: None):
        """
        Parameters
        ------------------------------------------
        ### Target Data
        The data to deep crawl from.
        Output will be from the same location as target data.

        ### Task Thread
        Check Core.Async.TaskThread. Only use it when calling this as a thread.

        """
        invalidArgs = False
        if not targetDataPath.strip():
            self.viewModelRef.ShowUserMessage("File Path should not be empty!")
            invalidArgs = True
        if not os.path.isfile(targetDataPath):
            self.viewModelRef.ShowUserMessage("Path to file does not exists!")
            invalidArgs = True

        jsonData = None;
        if not invalidArgs:
            try:
                jsonData = Database.OpenJsonData(targetDataPath)
            except:
                self.viewModelRef.ShowUserMessage("Given file is invalid! Not a JSON?")
                message = "Error converting user given file to JSON; NOTE: User has likely given an invalid data format."
                # TODO: Log include file content
                Log("Deep Crawl Data Read Error", message)
                invalidArgs = True

        if invalidArgs:
            if not taskThread == None:
                taskThread.isRunning = False
            return None
        # TODO: Reformat
        # These constants should be dynamic and loaded from somewhere
        # based on the requested site to crawl.
        deepCrawlList = jsonData["Stories"]
        if deepCrawlList == None or deepCrawlList == []:
            self.viewModelRef.ShowUserMessage("Given file is either invalid or has no data filled!")
            return None

        crawlSite = "https://www.scamalert.sg"

        jsonData = json.loads('{"Stories": []}')

        progress = 0
        for data in deepCrawlList:
            self.viewModelRef.UpdateLoadingBar((progress / len(deepCrawlList)) * 100)

            targetSite = crawlSite + data["Url"]
            contentRaw = self.Crawl(targetSite)
            print(contentRaw)

        self.viewModelRef.UpdateLoadingBar(100)
        if taskThread != None:
            taskThread.isRunning = False

    def Crawl(self, site: str) -> str:
        crawler = Crawler(site, None)
        return crawler.Crawl()

    def GetContentList(self, content:str, contentKey:str):
        # Get whatever is in '[]' after the contentKey
        content = content[content.index(contentKey):]
        content = content[content.index("[")+1:]
        content = content[:content.index("]")]

        # Split the string by each '{}'
        content = content.replace("},", "ia2sd3")
        contentArray = content.split("ia2sd3")
        for i in range(0,len(contentArray) - 2, 1):
            contentArray[i] += "}"

        return contentArray

    def RemoveNoiseFromContent(content: str) -> str:
        content = content.replace("\\u0026", "&")
        content = content.replace("\\u0027", "'")
        content = content.replace("\\xa0\\", " ")
        
        return content