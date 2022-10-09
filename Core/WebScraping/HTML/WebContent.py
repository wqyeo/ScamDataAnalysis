import os

from Core.Logging.Logger import *
from Core.Database import *
from Core.WebScraping.HTML.ScrapTarget import ScrapTarget


class WebContent:
    def __init__(self, tag: str, jsonName: str, class_:str = None, innerContents: list = None, storeTextContent: bool = True, contentSplit = None) -> None:
        """
        Represents a web content data.

        # Params
        --------------------------
        **tag**
        The HTML tag this content was under.

        **class_** *Optional*
        The class tag this content was under.

        **jsonName**
        The name to be classified under when this gets parsed to JSON.

        **innerContents** *Optional*
        The inner contents of this content.
        """
        self.tag = tag
        self.class_ = class_
        self.jsonName = jsonName
        self.innerContents = innerContents
        self.storeTextContent = storeTextContent
        self.contentSplit = None
        pass

    def CreateWebContentsByTarget(scrapTarget: ScrapTarget) -> list:
        configPath = os.path.join("Core", "WebScraping", "HTML", "Configs")

        if scrapTarget == ScrapTarget.SCAM_ALERT_STORIES:
            configPath = os.path.join(configPath, "ScamAlertStories.json")
        else:
            Log("Unimplemented Configuraiton", "Unimplemented HTML-Scrap Configuration for {}".format(scrapTarget.name), LogSeverity.WARNING)
            pass
        
        configs = None
        try:
            configs = Database.OpenJsonData(configPath)
        except:
            Log("Load configuration failed", "Failed to load HTML-Scrap Configuration from {}".format(scrapTarget.name), LogSeverity.ERROR)
            return None

        result = WebContent._LoadWebContent(configs["WebContents"])

        if result == None:
            Log("Configuration Invalid", "Loading HTML-Scrap Configuration of {} results in None. Invalid configuration.".format(scrapTarget.name), LogSeverity.ERROR)

        return result

    def _LoadWebContent(contentConfigs: list) -> list:
        result = []
        for config in contentConfigs:
            current = WebContent("", "")

            if not ("tag" in config) or not ("jsonName" in config):
                Log("Invalid configuration state", "One HTML-Scrap config state was invalid, skipping...", LogSeverity.WARNING)
                continue

            current.tag = config["tag"]
            current.jsonName = config["jsonName"]

            if "class_" in config:
                current.class_ = config["class_"]
            if "storeTextContent" in config:
                current.storeTextContent = config["storeTextContent"]
            if "innerContents" in config:
                current.innerContents = WebContent._LoadWebContent(config["innerContents"])
            if "contentSplit" in config:
                current.contentSplit = config["contentSplit"]
            result.append(current)
        
        if len(result) == 0:
            return None

        return result
