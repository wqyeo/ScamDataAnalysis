import json
import os
import requests
import http.client

from Core.Logging.Logger import *
from Core.Crawling.CrawlTarget import *
from Core.Database import Database

class Crawler:
    def __init__(self, site: str, data = None, noisePattern=None) -> None:
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
    
    def GetStraitsTime(self) -> str:
        conn = http.client.HTTPSConnection("www.straitstimes.com")
        payload = ''
        headers = {
        'Cookie': 'AWSALB=SLqvBOAaqPK2b4sczP+e0arLclECeiqtdcxiKy4bVrVwCkIj647sShmvVpWpdLCEGyHf1YWanisz/atsEP3U8Gad08/5pRbBbDp/IoPS4oOtTP1iTpykcJAgSKj5; AWSALBCORS=SLqvBOAaqPK2b4sczP+e0arLclECeiqtdcxiKy4bVrVwCkIj647sShmvVpWpdLCEGyHf1YWanisz/atsEP3U8Gad08/5pRbBbDp/IoPS4oOtTP1iTpykcJAgSKj5; sph_user_country=SG'
        }
        conn.request("GET", self.site.replace("https://www.channelnewsasia.com", ""), payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

    def GetChannelNewsAsia(self) -> str:
        payload={}
        headers = {
        'Cookie': 'incap_ses_1523_1015034=/yX5S4lTHmcrKJ2sr8giFUcQS2MAAAAApo6vIVaRsBzqFqre3fnB5g==; visid_incap_1015034=tC1R4m8TSTGKpmoJf/dkvzBFSmMAAAAAQUIPAAAAAAAygoeE6GnWAHWDIJ7gRnur'
        }

        response = requests.request("GET", self.site, headers=headers, data=payload)

        return response.text

    def CrawlGetRequest(self) -> str:
        try:
            if self.data != None:
                request = requests.get(self.site, data=self.data)
            else: 
                request = requests.get(self.site)
            content = request.text
            if not self.noisePattern == None:
                content = self.noisePattern(content)
            return content
        except:
            Log("Deflate Encoding", "Normal Encoding Failed, trying deflate", LogSeverity.LOG)
            # Try deflate encoding
            if self.data != None:
                self.data["Accept-Encoding"] = "deflate"
            else: 
                self.data = {'Accept-Encoding': 'deflate'}
            request = requests.get(self.site, data=self.data)
            content = request.text
            if not self.noisePattern == None:
                content = self.noisePattern(content)
            return content

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
        if crawlTarget == CrawlTarget.SCAM_ALERT_NEWS:
            filePath = os.path.join(configPath, "ScamAlertNews.json")
            return Database.OpenJsonData(filePath)
        else:
            return None