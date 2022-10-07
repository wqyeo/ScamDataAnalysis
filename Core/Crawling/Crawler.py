import json
import os
import requests

from Core.Crawling.CrawlTarget import *
from Core.Database import Database

class Crawler:
    def __init__(self, site, data = None, noisePattern=None) -> None:
        """
        Create an Object for crawling data with specific params.

        Params
        ----------------------

        ### site: string
        The site to crawl on.

        ### data: object
        Additional data to send on the site when doing HTTP request.

        ### noisePattern: function(str)
        Function to remove noise from content string
        """
        self.site = site
        self.data = data
        self.noisePattern = noisePattern
        pass

    def CrawlRaw(self) -> str:
        request = requests.post(self.site, data=self.data)
        content = request.text
        if not self.noisePattern == None:
            content = self.noisePattern(content)
        return content

    def Crawl(self) -> str:
        """
        Crawl through using the initial set params.

        # Returns
        The content of the site. In Raw string
        """

        request = requests.post(self.site, data=self.data)
        reqContent = self._GetContentFromRequest(request)
        if not self.noisePattern == None:
            reqContent = self.noisePattern(reqContent)

        return reqContent

    def _GetContentFromRequest(self, request: requests.Response) -> str:
        jsonObject = json.loads(request.text)
        return jsonObject["result"]

    def LoadConfig(crawlTarget: CrawlTarget) -> dict:
        configPath = os.path.join("Core", "Crawling", "Configs")
        if crawlTarget == CrawlTarget.SCAM_ALERT_STORIES:
            filePath = os.path.join(configPath, "ScamAlertStories.json")
            return Database.OpenJsonData(filePath)
        else:
            # TODO: Error or something
            pass