import os
from Lib.Crawler import Crawler

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

        self.viewModelRef.ShowUserMessage("")

        # TODO: Reformat
        crawlSite = "https://www.scamalert.sg/stories/GetStoryListAjax/get?scamType=&year=&month=&page=1&sortBy=Latest"
        crawlSiteData = {
            "scamType": "",
            "year": "",
            "month": "",
            "page": "2",
            "sortBy": "Latest"
        }

        crawler = Crawler(crawlSite, crawlSiteData)

        crawler.Crawl()