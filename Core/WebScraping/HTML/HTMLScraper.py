from bs4 import BeautifulSoup
from Core.Logging.LogSeverity import LogSeverity
from Core.Logging.Logger import Log

from Core.Util import *
from Core.WebScraping.HTML.WebContent import WebContent

class HTMLScraper:
    def __init__(self, htmlContent: str, webContents: list, contentIsSoup: bool = False) -> None:
        """
        Create a HTML Scraper to scrap through certain content based on 'WebContent' objects.

        # Params
        -----------------------------------------
        **htmlContent**
        The raw HTML content in string format.

        **webContents**
        A list of 'WebContent'.
        """
        if contentIsSoup:
            self.soup = htmlContent
        else:
            self.soup = BeautifulSoup(htmlContent, "html.parser")
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
            # TODO: SHould we log if its returning None?
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
            # Ignore if Content not found.
            if not content or content == None:
                continue

            # If this webcontent has inner.
            if webContent.innerContents != None:
                # Recursively scrap through each inner content
                innerScraper = HTMLScraper(content, webContent.innerContents, True)
                scrapped = innerScraper.Scrap()
                # Append if the inner has content.
                if scrapped != None:
                    toAppend = {}
                    toAppend.update(scrapped)
                    hasInner = True

                
            # Try append if requested.
            if webContent.storeTextContent:
                contentText = self._Clean(content.text)
                contentText = self._SplitContent(contentText, webContent.contentSplit)
                contentText = contentText.strip()

                # Append this webcontent text if not empty
                if not IsEmptyOrWhitespace(contentText):
                    if webContent.contentSplit != None:
                        for splitConfig in webContent.contentSplit:
                            splitConfig = splitConfig.split(",")

                    if hasInner:
                        toAppend["TextContent"] = contentText
                    else:
                        toAppend = contentText
            
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

    def _SplitContent(self, contentText: str, splitConfigs: list) -> str:
        if splitConfigs == None:
            return contentText

        for config in splitConfigs:
            try:
                config = config.split(",")

                if len(config) <= 1:
                    raise Exception("Config wrong")
                contentText = contentText.split(config[1])

                if config[0].lower() == "left":
                    contentText = contentText[0]
                else:
                    contentText = contentText[1]
            except:
                Log("HTML Scrapper Split Configuration", "One of the HTML Split Configuration is wrong, {}.".format(config), LogSeverity.LOG)
                return None
        return contentText

    def _Clean(self, content:str) -> str:
        # TODO: Load from config or smth
        content = content.replace('"', "'")
        content = content.strip().replace("\n", "").replace("\r", "")
        content = content.replace("\\", "")
        return content

    def _FindAll(self, webContent: WebContent) -> list:
        if webContent.class_ == None:
            return self.soup.find_all(webContent.tag)
        else:
            return self.soup.find_all(webContent.tag, class_=webContent.class_)