from Core.Analytics.WeightMap import WeightMap
from Core.Util import Lerp

PLATFORM_SEARCH_MAPPING = {
    "Telegram": [("telegram", 0.5)],
    "Facebook": [("facebook", 0.5), ("fb", 0.1)],
    "Whatsapp": [("whatsapp", 0.5), ("whatapps", 0.5)],
    "WeChat": [("wechat", 0.5)],
    "YouTube": [("youtube", 0.25)],
    "Phone Call": [("call", 0.025), ("dial", 0.01), ("number", 0.01)],
    "Tinder": [("tinder", 0.5)],
    "Instagram": [("insta", 0.5), ["ig", 0.1]]
}


def DeterminePlatform(description: str) -> str:
    description = description.lower()
    weightMap = WeightMap()

    for platform in PLATFORM_SEARCH_MAPPING:
        # For each keyword to find
        for keywordMapping in PLATFORM_SEARCH_MAPPING[platform]:
            firstOccurance = description.find(keywordMapping[0])
            counts = description.count(keywordMapping[0])

            # If there is an occurance
            if firstOccurance >= 0:
                # Determine weight by occurance location and counts.
                lerpVal = firstOccurance / len(description)
                weightVal = Lerp(0.001, keywordMapping[1], lerpVal) + ((counts / 10.0) * keywordMapping[1])
                weightMap.AddValueToWeight(platform, weightVal)

    # Find keyword with highest weight.
    result = weightMap.DetermineHighestWeight()
    if result == None:
        return "Unknown"
    return result