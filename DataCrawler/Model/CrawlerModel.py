import os

from Core.Crawler import Crawler
from Core.Database import Database

class CrawlerModel:
    def __init__(self, viewModelRef) -> None:
        self.viewModelRef = viewModelRef
        pass

    def CrawlAndSaveData(self, saveLocation: str):
        if not saveLocation.strip():
            self.viewModelRef.ShowUserMessage("Folder Path should not be empty!")
            return None
        if not os.path.isdir(saveLocation):
            self.viewModelRef.ShowUserMessage("Path to folder does not exists!")
            return None

        # TODO: Reformat
        # These constants should be dynamic and loaded from somewhere
        # based on the requested site to crawl.
        crawlSite = "https://www.scamalert.sg/stories/GetStoryListAjax/get?scamType=&year=&month=&page=1&sortBy=Latest"
        crawlSiteData = {
            "scamType": "",
            "year": "",
            "month": "",
            "page": "2",
            "sortBy": "Latest"
        }

        noisePattern = [
            "u0026hellip",
            "\\",
            "u0027"
        ]

        crawler = Crawler(crawlSite, crawlSiteData, noisePattern)
        content = crawler.Crawl()

        saveLocation = saveLocation + "/debug.json"
        Database.SaveData(content, saveLocation)

        self.viewModelRef.ShowUserMessage("Successfully saved under " + saveLocation)