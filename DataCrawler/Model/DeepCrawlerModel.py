import asyncio
from configparser import RawConfigParser
import os
import json
from Core.Crawling.CrawlTarget import CrawlTarget

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
    def CrawlAndSaveData(self, targetDataPath: str, taskThread = None):
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

        def GetCrawlTarget(data) -> CrawlTarget:
            for d in data:
                if d == "Stories":
                    return CrawlTarget.SCAM_ALERT_STORIES
                elif d == "News":
                    return CrawlTarget.SCAM_ALERT_NEWS

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

        if targetCrawl == "Stories":
            jsonData = self._CrawlStories(jsonData, webContents, taskThread)
        elif targetCrawl == "News":
            jsonData = self._CrawlNews(jsonData, webContents, taskThread)
        else:
            jsonData = None

        if jsonData != None:
            # File name should be similar as target data.
            originalFileName = os.path.basename(targetDataPath).split('/')[-1]
            saveFileName = "Detailed_" + originalFileName 
            # Save location same as where the target data is at.
            saveLocation = os.path.join(GetDirectoryFromFilePath(targetDataPath), saveFileName)

            Database.SaveJsonData(jsonData, saveLocation)

            self.viewModelRef.ShowUserMessage("Successfully saved under {}".format(saveLocation))
            self.viewModelRef.UpdateLoadingBar(100)
        FreeThread()

    def _CrawlNews(self, jsonData, webContents, taskThread = None):
#region Local_Function
        def FreeThread():
            nonlocal taskThread
            if taskThread != None:
                taskThread.isRunning = False
                self.viewModelRef.FreeAppThread()

        def ThreadStopSignalled():
            nonlocal taskThread
            if taskThread != None:
                return not taskThread.isRunning

        def TryGetListToCrawl() -> list:
            nonlocal jsonData
            res = None
            if "News" in jsonData:
                res = jsonData["News"]
            return res

        def DetermineScrapConfigByURL(url: str) -> str:
            if "channelnewsasia" in url:
                return "ChannelNewsAsia"
            elif "straitstimes" in url:
                return "StraitsTimes"
            elif "mothership.sg" in url:
                return "MothershipSG"
            return None
#endregion
        
        deepCrawlList = TryGetListToCrawl()
        if deepCrawlList == None:
            self.viewModelRef.ShowUserMessage("Given file is either invalid or has no data filled!")
            return None
        
        jsonData = json.loads('{"DetailedNews": []}')

        progress = 0
        for data in deepCrawlList:
            self._ShowCrawlingMessage()

            if ThreadStopSignalled():
                FreeThread()
                Log("Thread stop signal recieved.", "Receieved a Thread stop signal on {}".format(taskThread.name), LogSeverity.DEBUG)
                return None

            self.viewModelRef.UpdateLoadingBar((progress / len(deepCrawlList)) * 100)

            targetSite = data["Url"]
            configKey = DetermineScrapConfigByURL(targetSite)
            if configKey == None:
                Log("Unknown URL to Scrap", "Unknown URL to Scral for target site {}.".format(targetSite), LogSeverity.WARNING)
                continue

            try:
                contentRaw = None
                if configKey == "ChannelNewsAsia":
                    contentRaw = Crawler(targetSite, None).GetChannelNewsAsia()
                elif configKey == "StraitsTimes":
                    contentRaw = Crawler(targetSite, None).GetStraitsTime()
                else:
                    contentRaw = Crawler(targetSite, None).CrawlGetRequest()
            except:
                Log("URL Crawl Failed", "Failed to crawl URL {}".format(targetSite), LogSeverity.WARNING)
                continue

            scraper = HTMLScraper(contentRaw, webContents[configKey])
            content = scraper.Scrap()
            if content == None:
                continue

            try:
                date = data["Date"]
                if configKey == "ChannelNewsAsia":
                    texts = content["Text"]
                    if isinstance(texts, list):
                        desc = ""
                        for text in texts:
                            desc += text["Description"] + " "
                    else:
                        desc = texts

                    if desc == None:
                        raise Exception("Desc not found.")
                    desc = desc.strip()
                    content = {
                        "Date": date,
                        "Description": desc
                    }
                else:
                    content["Date"] = date

                if isinstance(content["Description"], list):
                    desc = ""
                    for text in content["Description"]:
                        desc += text + " "
                    desc = desc.strip()
                    content["Description"] = desc
            except:
                LogAndDump("Content Format", "Failed to format content.", contentRaw, LogSeverity.WARNING)
                continue
            
            try:
                jsonData["DetailedNews"].append(content)
            except:
                infoFileName = DumpInfo(content, LogSeverity.ERROR)
                message = "Error Converting one of scrapped data to JSON. More details at {}".format(infoFileName)
                Log("JSON Data Conver Error {}".format(data["Title"]), message, LogSeverity.ERROR)
                continue

            progress += 1       
        return jsonData

    def _CrawlStories(self, jsonData, webContents, taskThread = None):
#region Local_Function
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

        deepCrawlList = jsonData["Stories"]
        if "Stories" in jsonData:
            if deepCrawlList == None or deepCrawlList == []:
                self.viewModelRef.ShowUserMessage("Given file is either invalid or has no data filled!")
                return None
        else:
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
            contentRaw = Crawler(targetSite, None).CrawlRaw()

            scraper = HTMLScraper(contentRaw, webContents["ScamAlertStories"])
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
        return jsonData

    def _CreateWebContent(self, targetCrawl: str) -> list:
        targetType = None
        if targetCrawl.strip() == "Stories":
            targetType = ScrapTarget.SCAM_ALERT_STORIES
        elif targetCrawl.strip() == "News":
            targetType = ScrapTarget.SCAM_ALERT_NEWS
        else:
            return None

        return WebContent.CreateWebContentsByTarget(targetType)