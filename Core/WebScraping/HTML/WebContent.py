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

    def CreateWebContentsByTarget(scrapTarget: ScrapTarget) -> dict:
#region Local_Function
        def TryGetConfigsFromPaths(pathList: list) -> list:
            res = []
            for path in pathList:
                try:
                    res.append(Database.OpenJsonData(path))
                except:
                    return None
            return res

        def GetWebContentFromConfigs(confList: list) -> dict:
            res = {}
            for confg in confList:
                try:
                    for key in confg:
                        curr = WebContent._LoadWebContent(confg[key])
                        if curr == None:
                            raise Exception("Invalid Configuration")
                        res[key] = curr
                        # Cause there will only be one key, else the configuration would be invalid.
                        break
                except:
                    LogAndDump("Configuration Invalid", "Loading HTML-Scrap Configuration for {} is Invalid.".format(scrapTarget), confg, LogSeverity.WARNING)
                    continue
            return res
#endregion

        configPath = os.path.join("Core", "WebScraping", "HTML", "Configs")

        configPaths = []
        if scrapTarget == ScrapTarget.SCAM_ALERT_STORIES:
            configPaths.append(os.path.join(configPath, "ScamAlertStories.json"))
        elif scrapTarget == ScrapTarget.SCAM_ALERT_NEWS:
            configPaths.append(os.path.join(configPath, "ChannelNewsAsia.json"))
            configPaths.append(os.path.join(configPath, "MothershipSG.json"))
            configPaths.append(os.path.join(configPath, "StraitsTimes.json"))
        else:
            Log("Unimplemented Configuraiton", "Unimplemented HTML-Scrap Configuration for {}".format(scrapTarget.name), LogSeverity.WARNING)
            return None
        
        configs = TryGetConfigsFromPaths(configPaths)
        if configs == None:
            Log("Load configuration failed", "Failed to load HTML-Scrap Configuration from {}".format(scrapTarget.name), LogSeverity.ERROR)
            return None

        result = GetWebContentFromConfigs(configs)
        if len(result) == 0:
            Log("Configuration Invalid", "Loading HTML-Scrap Configuration of {} results in None. Invalid configuration.".format(scrapTarget.name), LogSeverity.ERROR)
            return None

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
