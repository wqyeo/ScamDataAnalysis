import os

from Core.Crawler import Crawler
from Core.Database import Database

class CrawlerModel:
    def __init__(self, viewModelRef) -> None:
        self.viewModelRef = viewModelRef
        pass

    def CrawlAndSaveData(self, saveLocation: str, recursiveTimes: int):
        """
        Parameters
        ------------------------------------------
        ### Save Location
        The target folder where the user want to save the data in.

        ### Recursive Times
        How many pages it will crawl through
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
