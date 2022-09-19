import json
import requests

class Crawler:
    def __init__(self, site, data = None, noiseStr = []) -> None:
        """
        Create an Object for crawling data with specific params.

        Params
        ----------------------

        ### site: string
        The site to crawl on.

        ### data: object
        Additional data to send on the site when doing HTTP request.

        ### noiseStr: string[]
        Remove all text from content that matches with this noise string list.
        """
        self.site = site
        self.data = data
        self.noiseStr = noiseStr
        pass

    def Crawl(self) -> str:
        """
        Crawl through using the initial set params.

        # Returns
        The content of the site. In Raw string
        """

        request = requests.post(self.site, data=self.data)
        reqContent = self._GetContentFromRequest(request)
        reqContent = self._FilterOutNoise(reqContent)

        return reqContent

    def _FilterOutNoise(self, content: str) -> str:
        for noisePattern in self.noiseStr:
            content = content.replace(noisePattern, "")
        return content

    def _GetContentFromRequest(self, request: requests.Response) -> str:
        jsonObject = json.loads(request.text)
        return jsonObject["result"]