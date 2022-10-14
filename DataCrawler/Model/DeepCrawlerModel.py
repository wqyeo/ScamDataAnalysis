import asyncio
from configparser import RawConfigParser
import os
import json

from Core.Logging.Logger import *
from Core.Crawling.Crawler import Crawler
from Core.Database import Database

from Core.WebScraping.HTML.HTMLScraper import *
from Core.WebScraping.HTML.WebContent import *

class DeepCrawlerModel:
    def __init__(self, viewModelRef) -> None:
        self.viewModelRef = viewModelRef
        self._crawlingMessageCycle = 1
        pass

    def _ShowCrawlingMessage(self):
        self._crawlingMessageCycle += 1
        if self._crawlingMessageCycle >= 4:
            self._crawlingMessageCycle = 1
        self.viewModelRef.ShowUserMessage("Crawling" + ("." * self._crawlingMessageCycle))

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

#region Local_Functions

        def FreeThread():
            nonlocal taskThread
            if taskThread != None:
                taskThread.isRunning = False
                self.viewModelRef.FreeAppThread()

        def ThreadStopSignalled():
            nonlocal taskThread
            if taskThread != None:
                return not taskThread.isRunning

#endregion

        # Check if valid file path
        invalidArgs = not IsValidFilePath(targetDataPath)
        if invalidArgs:
            self.viewModelRef.ShowUserMessage("Given File Path is invalid!")
            FreeThread()
            return None

        # Check if valid JSON File
        jsonData = None
        targetCrawl = None
        webContents = None
        if not invalidArgs:
            try:
                jsonData = Database.OpenJsonData(targetDataPath)
                targetCrawl = list(jsonData.keys())[0]
                webContents = self._CreateWebContent(targetCrawl)

                if webContents == None:
                    Log("Deep Crawl Unknown Data", "User gave a valid JSON file, but unknown data to parse, {}".format(targetCrawl))
                    self.viewModelRef.ShowUserMessage("Unknown contents in given JSON file.")
                    invalidArgs = True
            except:
                self.viewModelRef.ShowUserMessage("Given file is invalid! Not a JSON?")
                message = "Error converting user given file to JSON; NOTE: User has likely given an invalid data format."
                # TODO: Log include file content
                Log("Deep Crawl Data Read Error", message)
                invalidArgs = True

        # Either Invalid JSON File or File path.
        if invalidArgs:
            FreeThread()
            return None

        # TODO: Reformat
        # These constants should be dynamic and loaded from somewhere
        # based on the requested site to crawl.
        deepCrawlList = jsonData["Stories"]
        if deepCrawlList == None or deepCrawlList == []:
            self.viewModelRef.ShowUserMessage("Given file is either invalid or has no data filled!")
            return None

        crawlSite = "https://www.scamalert.sg"

        jsonData = json.loads('{"DetailedStories": []}')

        progress = 0
        for data in deepCrawlList:
            self._ShowCrawlingMessage()
            if ThreadStopSignalled():
                FreeThread()
                Log("Thread stop signal recieved.", "Receieved a Thread stop signal on {}".format(taskThread.name), LogSeverity.DEBUG)
                return None

            self.viewModelRef.UpdateLoadingBar((progress / len(deepCrawlList)) * 100)

            targetSite = crawlSite + data["Url"]
            contentRaw = self._Crawl(targetSite)

            scraper = HTMLScraper(contentRaw, webContents)
            content = scraper.Scrap()
            if content == None:
                continue
            
            try:
                jsonData["DetailedStories"].append(content)
            except:
                infoFileName = DumpInfo(content, LogSeverity.ERROR)
                message = "Error Converting one of scrapped data to JSON. More details at {}".format(infoFileName)
                Log("JSON Data Conver Error {}".format(data["Title"]), message, LogSeverity.ERROR)
                continue

            progress += 1

        # File name should be similar as target data.
        originalFileName = os.path.basename(targetDataPath).split('/')[-1]
        saveFileName = "Detailed_" + originalFileName
        # Save location same as where the target data is at.
        saveLocation = os.path.join(GetDirectoryFromFilePath(targetDataPath), saveFileName)

        Database.SaveJsonData(jsonData, saveLocation)

        self.viewModelRef.ShowUserMessage("Successfully saved under {}".format(saveLocation))
        self.viewModelRef.UpdateLoadingBar(100)
        FreeThread()

    def _Crawl(self, site: str) -> str:
        crawler = Crawler(site, None)
        return crawler.CrawlRaw()

    def _CreateWebContent(self, targetCrawl: str) -> list:
        targetType = None
        if targetCrawl.strip() == "Stories":
            targetType = ScrapTarget.SCAM_ALERT_STORIES
        else:
            return None

        return WebContent.CreateWebContentsByTarget(targetType)