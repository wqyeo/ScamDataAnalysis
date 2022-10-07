import json
from bs4 import BeautifulSoup

from Core.Util import *
from Core.WebScraping.HTML.WebContent import WebContent

class HTMLScraper:
    def __init__(self, htmlContent: str, webContents: list) -> None:
        """
        Create a HTML Scraper to scrap through certain content based on 'WebContent' objects.

        # Params
        -----------------------------------------
        **htmlContent**
        The raw HTML content in string format.

        **webContents**
        A list of 'WebContent'.
        """
        self.soup = BeautifulSoup(htmlContent)
        self.webContents = webContents
        pass

    def Scrap(self) -> dict:
        result = {}
        for webContent in self.webContents:
            scrapped = self._ScrapContent(webContent)

            if not scrapped or scrapped != None:
                result[webContent.jsonName] = scrapped

        if result or result != None:
            return result
        else:
            return None

    def _ScrapContent(self, webContent:WebContent):
        result = None
        rawContent = self._FindAll(webContent)

        if rawContent == None or not rawContent:
            return None

        result = []
        # Assuming there is multiple content.
        for content in rawContent:
            toAppend = None
            hasInner = False
            # If this webcontent has inner.
            if webContent.innerContents != None:
                # Recursively scrap through each inner content
                innerScraper = HTMLScraper(content, webContent.innerContents)
                scrapped = innerScraper.Scrap()
                # Append if the inner has content.
                if scrapped != None:
                    toAppend = {}
                    toAppend.update(scrapped)
                    hasInner = True
                
            # Append this webcontent if its not empty.
            if not IsEmptyOrWhitespace(content.text):
                if hasInner:
                    toAppend["text_content"] = content.text
                else:
                    toAppend = content.text
            
            # Append to result if this content is not empty.
            if toAppend != None or not toAppend:
                result.append(toAppend)

        # If there is only 1 result in the list
        # We want to only result the 1 element.
        # (Prevents returning a list of only 1 element.)        
        if len(result) == 1:
            result = result[0]
    
        # There is at least one content to return
        if result and result != None:
            return result
        else:
            return None


    def _FindAll(self, webContent: WebContent) -> list:
        if webContent.class_ == None:
            return self.soup.find_all(webContent.tag)
        else:
            return self.soup.find_all(webContent.tag, class_=webContent.class_)