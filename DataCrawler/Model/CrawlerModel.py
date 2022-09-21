import asyncio
import os
import json
import ast

from Core.Crawler import Crawler
from Core.Database import Database

class CrawlerModel:
    def __init__(self, viewModelRef) -> None:
        self.viewModelRef = viewModelRef
        pass

    @asyncio.coroutine
    def CrawlAndSaveData(self, saveLocation: str, recursiveTimes: int, taskThread: None):
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
        if not saveLocation.strip():
            self.viewModelRef.ShowUserMessage("Folder Path should not be empty!")
            return None
        if not os.path.isdir(saveLocation):
            self.viewModelRef.ShowUserMessage("Path to folder does not exists!")
            return None

        # TODO: Reformat
        # These constants should be dynamic and loaded from somewhere
        # based on the requested site to crawl.
        crawlSite = "https://www.scamalert.sg/stories/GetStoryListAjax/"
        crawlSiteData = {
            "scamType": "",
            "year": "",
            "month": "",
            "page": "1",
            "sortBy": "Latest"
        }

        jsonData = json.loads('{"Stories": []}')

        # Recursively crawl and fetch raw content (string)
        for pageNo in range(recursiveTimes):
            self.viewModelRef.UpdateLoadingBar((pageNo / recursiveTimes) * 100)

            crawlSiteData["page"] = str(pageNo)
            contentRaw = self.Crawl(crawlSite, crawlSiteData)

            # Try to get the raw contents as an array.
            contentArray = None
            try:
                contentArray = self.GetContentList(contentRaw, "StoryList")
            except:
                # TODO: Proper logging.
                print("Error fetching data at page: " + str(pageNo))
                continue

            for content in contentArray:
                # Try to read each content as JSON.
                try:
                    tempJson = json.loads(content)
                except:
                    print("Error converting one of the data at page " + str(pageNo) + " to JSON Data.")
                    continue

                jsonData["Stories"].append(tempJson)

        # TODO: Proper generation for file-name rather than 'debug.json'
        saveLocation = saveLocation + "/debug.json"
        Database.SaveJsonData(jsonData, saveLocation)

        self.viewModelRef.ShowUserMessage("Successfully saved under " + saveLocation)
        self.viewModelRef.UpdateLoadingBar(100)
        if taskThread != None:
            taskThread.isRunning = False

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