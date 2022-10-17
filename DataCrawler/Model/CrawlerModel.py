import os
import json
import asyncio
import datetime

from Core.Crawling.CrawlTarget import CrawlTarget
from Core.Logging.Logger import *
from Core.Crawling.Crawler import Crawler
from Core.Database import Database
from Core.Util import IsValidDirectory

class CrawlerModel:
    def __init__(self, viewModelRef) -> None:
        self.viewModelRef = viewModelRef
        self._crawlingMessageCycle = 1
        pass

    def _ShowCrawlingMessage(self):
        self._crawlingMessageCycle += 1
        if self._crawlingMessageCycle >= 4:
            self._crawlingMessageCycle = 1
        self.viewModelRef.ShowUserMessage("Crawling" + ("." * self._crawlingMessageCycle))

    def _DoCrawlAndSave(self, saveLocation: str, recursiveTimes: int, targetCrawlSite: str, taskThread = None):
#region LocalFunction
        def FreeThread():
            nonlocal taskThread
            if taskThread != None:
                taskThread.isRunning = False
                self.viewModelRef.FreeAppThread()

        def ThreadStopSignalled() -> bool:
            nonlocal taskThread
            if taskThread != None:
                return not taskThread.isRunning

        def GetJSONHeader(crawlTarget: CrawlTarget):
            if crawlTarget == CrawlTarget.SCAM_ALERT_STORIES:
                return "Stories"
            elif crawlTarget == CrawlTarget.SCAM_ALERT_NEWS:
                return "News"
            return ""

        def GetContentListKey(crawlTarget: CrawlTarget) -> str:
            listKey = ""
            if crawlTarget == CrawlTarget.SCAM_ALERT_NEWS:
                listKey = "NewsList"
            elif crawlTarget == CrawlTarget.SCAM_ALERT_STORIES:
                listKey = "StoryList"
            return listKey
#endregion
        # Check if Save Location exists
        invalidArgs = not IsValidDirectory(saveLocation)
        if invalidArgs:
            self.viewModelRef.ShowUserMessage("Path to Save data at is invalid.")
            FreeThread()
            return None

        crawlTarget = CrawlerModel._GetCrawlTarget(targetCrawlSite)
        # Load target Site and Headers from configuration.
        crawlConfig = CrawlerModel._GetTargetCrawlSiteConfig(crawlTarget)
        if crawlConfig == None:
            Log("Crawl Config Invalidation", "Crawl Config is invalid from the parm: {}".format(targetCrawlSite))
            invalidArgs = True

        # End if any of the passed arguments is invalid
        if invalidArgs:
            FreeThread()
            return None

        if not ("Site" in crawlConfig and "Headers" in crawlConfig):
            Log("Config missing keys", "CrawlConfig is missing keys", LogSeverity.WARNING)
            return None
        crawlSite = crawlConfig["Site"]
        crawlSiteHeaders = crawlConfig["Headers"]

        jsonHeader = GetJSONHeader(crawlTarget)
        jsonData = json.loads('{"' + jsonHeader + '": []}')
        # Recursively crawl and fetch raw content (string)
        for pageNo in range(recursiveTimes):
            self._ShowCrawlingMessage()
            # This thread stop signal is send
            if ThreadStopSignalled():
                FreeThread()
                Log("Thread stop signal recieved.", "Receieved a Thread stop signal on {}".format(taskThread.name), LogSeverity.DEBUG)
                return None
            
            self.viewModelRef.UpdateLoadingBar((pageNo / recursiveTimes) * 100)

            if not ("page" in crawlSiteHeaders):
                Log("Config missing keys", "CrawlConfig is missing keys of 'page'", LogSeverity.WARNING)
                return None

            # Try to get the raw contents as an array.
            contentArray = None
            try:
                crawlSiteHeaders["page"] = str(pageNo)
                contentRaw = self._Crawl(crawlSite, crawlSiteHeaders)

                listKey = GetContentListKey(crawlTarget)
                contentArray = self._GetContentList(contentRaw, listKey)
            except:
                if contentRaw != None:
                    infoFileName = DumpInfo(contentRaw, LogSeverity.WARNING)
                    message = "Error Fetching data at page: {pageNo}. More info at {fileName}.".format(pageNo=pageNo, fileName=infoFileName)
                else:
                    message = "Error Fetching data at page: {pageNo}. No info was gathered as the crawl did not return any raw data.".format(pageNo=pageNo)
                Log("Page Fetch Data", message, LogSeverity.WARNING)
                continue

            if contentArray == None:
                Log("None ContentArray", "ContentArray was None in CrawlerModel at page {pageNo}.".format(pageNo=pageNo), LogSeverity.WARNING)
                continue

            for content in contentArray:
                if content == None:
                    continue

                content = content.strip()
                if content == "":
                    continue
                # Try to read each content as JSON.
                try:
                    # NOTE: Attempts to fix some of the JSON file not ending with } properly.
                    if content[-1] != "}":
                        content += "}"
                    tempJson = json.loads(content)
                except:
                    infoFileName = DumpInfo(content, LogSeverity.WARNING)
                    message = "Error Converting one data to JSON at page: {pageNo}. More info at {fileName}.".format(pageNo=pageNo, fileName=infoFileName)
                    Log("Data Convert", message, LogSeverity.WARNING)
                    continue

                jsonData[jsonHeader].append(tempJson)

        fileName = CrawlerModel._GenerateFileName(crawlTarget)
        saveLocation = os.path.join(saveLocation, fileName)
        Database.SaveJsonData(jsonData, saveLocation)

        self.viewModelRef.ShowUserMessage("Successfully saved under " + saveLocation)
        self.viewModelRef.UpdateLoadingBar(100)
        FreeThread()

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
        try:
            self._DoCrawlAndSave(saveLocation, recursiveTimes, targetCrawlSite, taskThread)
        except Exception as e:
            Log("Unhandled CrawlerModel Exception", "Unhandled exception, {}".format(getattr(e, 'message', repr(e))), LogSeverity.SEVERE)
            self.viewModelRef.ShowUserMessage("Woops, a severe error occured! Check LogDump for more info.")
        finally:
            if taskThread != None:
                taskThread.isRunning = False
                self.viewModelRef.FreeAppThread()

    def _GenerateFileName(crawlTarget: CrawlTarget) -> str:
        # Crawl Type - Datetime - .json
        return crawlTarget.name + "_" + (datetime.datetime.now().strftime("%Y-%B-%d_%H-%M-%S")) + ".json"

    def _GetCrawlTarget(targetCrawlSite: str) -> CrawlTarget:
        targetCrawlSite = targetCrawlSite.strip()
        crawlTarget = None
        if targetCrawlSite == "ScamAlert - Stories":
            crawlTarget = CrawlTarget.SCAM_ALERT_STORIES
        elif targetCrawlSite == "ScamAlert - News":
            crawlTarget = CrawlTarget.SCAM_ALERT_NEWS

        return crawlTarget

    def _GetTargetCrawlSiteConfig(crawlTarget: CrawlTarget) -> dict: 
        if crawlTarget == None:
            return None

        # Load target Site and Headers from configuration.
        return Crawler.LoadConfig(crawlTarget)

    def _Crawl(self, site: str, data: object) -> str:
        crawler = Crawler(site, data, CrawlerModel.RemoveNoiseFromContent)
        return crawler.Crawl()

    def _GetContentList(self, content:str, contentKey:str):
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
        content = content.replace('\\"', "'")
        content = content.replace("\\u0026", "&")
        content = content.replace("\\u0027", "'")
        content = content.replace(chr(0x2019), "'")
        content = content.replace("\\xa0\\", " ")
        
        return content