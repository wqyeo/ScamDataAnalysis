import asyncio
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

    def _DoCrawlAndSave(self, targetDataPath: str, taskThread = None):
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
        if not IsValidFilePath(targetDataPath):
            self.viewModelRef.ShowUserMessage("Given File Path is invalid!")
            FreeThread()
            return None

        # Check if valid JSON File
        jsonData = None
        targetCrawl = None
        webContents = None
        try:
            jsonData = Database.OpenJsonData(targetDataPath)
            targetCrawl = list(jsonData.keys())[0]
            webContents = self._CreateWebContent(targetCrawl)

            if webContents == None:
                Log("Deep Crawl Unknown Data", "User gave a valid JSON file, but unknown data to parse, {}".format(targetCrawl))
                self.viewModelRef.ShowUserMessage("Unknown contents in given JSON file.")
        except:
            self.viewModelRef.ShowUserMessage("Given file is invalid! Not a JSON?")
            message = "Error converting user given file to JSON; NOTE: User has likely given an invalid data format."
            # TODO: Log include file content
            Log("Deep Crawl Data Read Error", message)

        # Either Invalid JSON File or File path.
        if jsonData == None or targetCrawl == None or webContents == None:
            FreeThread()
            return None

        if targetCrawl == "Stories":
            jsonData = self._CrawlStories(jsonData, webContents, taskThread)
        elif targetCrawl == "News":
            jsonData = self._CrawlNews(jsonData, webContents, taskThread)
        else:
            jsonData = None

        if jsonData != None:
            try:
                # File name should be similar as target data.
                originalFileName = os.path.basename(targetDataPath).split('/')[-1]
                saveFileName = "Detailed_" + originalFileName 
                # Save location same as where the target data is at.
                saveLocation = os.path.join(GetDirectoryFromFilePath(targetDataPath), saveFileName)

                Database.SaveJsonData(jsonData, saveLocation)
                self.viewModelRef.ShowUserMessage("Successfully saved under {}".format(saveLocation))
                self.viewModelRef.UpdateLoadingBar(100)
            except Exception as e:
                Log("Failed to save JSON Data", "Failed to save JsonData in DeepCrawler, message {}".format(getattr(e, 'message', repr(e))), LogSeverity.ERROR)
                self.viewModelRef.ShowUserMessage("Failed to save crawled Data!")
        FreeThread()

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
        try:
            self._DoCrawlAndSave(targetDataPath, taskThread)
        except Exception as e:
            Log("Unhandled DeepCrawlerModel Exception", "Unhandled exception, {}".format(getattr(e, 'message', repr(e))), LogSeverity.SEVERE)
            self.viewModelRef.ShowUserMessage("Woops, a severe error occured! Check LogDump for more info.")
        finally:
            if taskThread != None:
                taskThread.isRunning = False
                self.viewModelRef.FreeAppThread()

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

        def TryGetRawContentFromSite(targetSite: str, configKey: str):
            contentRaw = None
            try:
                if configKey == "ChannelNewsAsia":
                    contentRaw = Crawler(targetSite, None).GetChannelNewsAsia()
                elif configKey == "StraitsTimes":
                    contentRaw = Crawler(targetSite, None).GetStraitsTime()
                else:
                    contentRaw = Crawler(targetSite, None).CrawlGetRequest()
            except:
                Log("URL Crawl Failed", "Failed to crawl URL {}".format(targetSite), LogSeverity.WARNING)
            return contentRaw

        def TryGetContentFromChannelNewsAsia(content: dict) -> dict:
            if not "Text" in content:
                LogAndDump("Text not found", "Text not found in web content.", content, LogSeverity.WARNING)
                return None

            texts = content["Text"]
            # If the text is a list of description
            # we iterate through and append it into 1 singluar string.
            if isinstance(texts, list):
                Log("Text is List", "Text is a list, iterating through each description", LogSeverity.LOG)
                desc = ""
                for text in texts:
                    if not "Description" in text:
                        LogAndDump("Description not found", "Description not found in text content.", text, LogSeverity.WARNING)
                        continue
                    desc += text["Description"] + " "
            else:
                desc = texts

            if desc == None:
                return None

            desc = desc.strip()
            content = {
                "Date": date,
                "Description": desc
            }
            return content
#endregion
        
        deepCrawlList = TryGetListToCrawl()
        if deepCrawlList == None:
            self.viewModelRef.ShowUserMessage("Given file is either invalid or has no data filled!")
            return None
        
        jsonData = json.loads('{"DetailedNews": []}')

        progress = 0
        for data in deepCrawlList:
            if data == None:
                continue
            self._ShowCrawlingMessage()
            self.viewModelRef.UpdateLoadingBar((progress / len(deepCrawlList)) * 100)

            if ThreadStopSignalled():
                FreeThread()
                Log("Thread stop signal recieved.", "Receieved a Thread stop signal on {}".format(taskThread.name), LogSeverity.DEBUG)
                return None

            if not "Url" in data:
                LogAndDump("Url not found", "Url not found in data.", data, LogSeverity.WARNING)
                continue

            targetSite = data["Url"]
            configKey = DetermineScrapConfigByURL(targetSite)
            if configKey == None:
                Log("Unknown URL to Scrap", "Unknown URL to Scrap for target site {}.".format(targetSite), LogSeverity.WARNING)
                continue

            contentRaw = TryGetRawContentFromSite(targetSite, configKey)
            if contentRaw == None:
                continue

            content = DeepCrawlerModel._TryScrapWebContent(contentRaw, webContents, configKey)
            if content == None:
                continue

            try:
                if not "Date" in data:
                    LogAndDump("Date not found", "Date not found in data.", data, LogSeverity.WARNING)
                    continue

                date = data["Date"]
                if configKey == "ChannelNewsAsia":
                    content = TryGetContentFromChannelNewsAsia(content)
                    if content == None:
                        continue
                else:
                    content["Date"] = date

                if not "Description" in content:
                    LogAndDump("Missing Description in content", "Missing Description in content.", content, LogSeverity.WARNING)
                    continue

                # If the description is a list,
                # merge them together to a single string.
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
            if data == None:
                continue
            if not "Url" in data:
                LogAndDump("Missing URL", "Missing URL in data.", data, LogSeverity.WARNING)
                continue

            
            targetSite = crawlSite + data["Url"]
            contentRaw = DeepCrawlerModel._TryCrawlSite(targetSite)
            if contentRaw == None:
                continue

            content = DeepCrawlerModel._TryScrapWebContent(contentRaw, webContents, "ScamAlertStories")
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
        
    def _TryScrapWebContent(rawContent, webContents, key):
        if rawContent == None:
            return None

        content = None
        try:
            scraper = HTMLScraper(rawContent, webContents[key])
            content = scraper.Scrap()
        except Exception as e:
            message = "Failed to scrap content from site. Error Message: {eMsg}.".format(eMsg=getattr(e, 'message', repr(e)))
            LogAndDump("Failed to scrap content", message, rawContent, LogSeverity.WARNING)
        return content

    def _TryCrawlSite(targetSite: str):
        contentRaw = None
        try:
            contentRaw = Crawler(targetSite, None).CrawlRaw()
        except Exception as e:
            message = "Failed to fetch content from site: {site}. Error Message: {eMsg}.".format(site=targetSite, eMsg=getattr(e, 'message', repr(e)))
            Log("Failed to fetch site content", message, LogSeverity.WARNING)
        return contentRaw