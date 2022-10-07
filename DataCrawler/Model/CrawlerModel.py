import asyncio
import os
import json
from Core.Crawling.CrawlTarget import CrawlTarget

from Core.Logging.Logger import *
from Core.Crawling.Crawler import Crawler
from Core.Database import Database

class CrawlerModel:
    def __init__(self, viewModelRef) -> None:
        self.viewModelRef = viewModelRef
        pass

    @asyncio.coroutine
    def CrawlAndSaveData(self, saveLocation: str, recursiveTimes: int, targetCrawlSite: str, taskThread = None):
        """
        Parameters
        ------------------------------------------
        ### Save Location
        The target folder where the user want to save the data in.

        ### Recursive Times
        How many pages it will crawl through

        ### Task Thread
        Check Core.Async.TaskThread. Only use it when calling this as a thread.

        """

        #region LocalFunction
        def FreeThread():
            nonlocal taskThread
            if taskThread != None:
                taskThread.isRunning = False
        #endregion

        print("run")
        invalidArgs = False
        # Check if Save Location exists
        if not saveLocation.strip():
            self.viewModelRef.ShowUserMessage("Folder Path should not be empty!")
            invalidArgs = True
        elif not os.path.isdir(saveLocation):
            self.viewModelRef.ShowUserMessage("Path to folder does not exists!")
            invalidArgs = True

        # Load target Site and Headers from configuration.
        crawlConfig = CrawlerModel._GetTargetCrawlSiteConfig(targetCrawlSite)
        if crawlConfig == None:
            Log("Crawl Config Invalidation", "Crawl Config is invalid from the parm: {}".format(targetCrawlSite))
            invalidArgs = True

        # End if any of the passed arguments is invalid
        if invalidArgs:
            FreeThread()
            return None

        crawlSite = crawlConfig["Site"]
        crawlSiteHeaders = crawlConfig["Headers"]

        jsonData = json.loads('{"Stories": []}')

        # Recursively crawl and fetch raw content (string)
        for pageNo in range(recursiveTimes):
            self.viewModelRef.UpdateLoadingBar((pageNo / recursiveTimes) * 100)

            crawlSiteHeaders["page"] = str(pageNo)
            contentRaw = self.Crawl(crawlSite, crawlSiteHeaders)

            # Try to get the raw contents as an array.
            contentArray = None
            try:
                contentArray = self.GetContentList(contentRaw, "StoryList")
            except:
                infoFileName = DumpInfo(contentRaw)
                message = "Error Fetching data at page: {pageNo}. More info at {fileName}.".format(pageNo=pageNo, fileName=infoFileName)
                Log("Page Fetch Data Error", message, LogSeverity.ERROR)
                continue

            for content in contentArray:
                # Try to read each content as JSON.
                try:
                    tempJson = json.loads(content)
                except:
                    infoFileName = DumpInfo(content, LogSeverity.ERROR)
                    message = "Error Converting one data to JSON at page: {pageNo}. More info at {fileName}.".format(pageNo=pageNo, fileName=infoFileName)
                    Log("Data Convert Error", message, LogSeverity.ERROR)
                    continue

                jsonData["Stories"].append(tempJson)

        # TODO: Proper generation for file-name rather than 'debug.json'
        saveLocation = saveLocation + "/debug.json"
        Database.SaveJsonData(jsonData, saveLocation)

        self.viewModelRef.ShowUserMessage("Successfully saved under " + saveLocation)
        self.viewModelRef.UpdateLoadingBar(100)
        FreeThread()

    def _GetTargetCrawlSiteConfig(targetCrawlSite: str) -> dict:
        targetCrawlSite = targetCrawlSite.strip()
        crawlTarget = None
        if targetCrawlSite == "ScamAlert - Stories":
            crawlTarget = CrawlTarget.SCAM_ALERT_STORIES
        elif targetCrawlSite == "ScamAlert - News":
            crawlTarget = CrawlTarget.SCAM_ALERT_NEWS
        
        if crawlTarget == None:
            return None

        # Load target Site and Headers from configuration.
        return Crawler.LoadConfig(CrawlTarget.SCAM_ALERT_STORIES)

    def Crawl(self, site: str, data: object) -> str:
        crawler = Crawler(site, data, CrawlerModel.RemoveNoiseFromContent)
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