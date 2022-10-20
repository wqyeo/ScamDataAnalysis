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
    "Instagram": [("insta", 0.5), ["ig", 0.1]],
    "Email": [("email", 0.4)],
    "SMS": [("message", 0.025), ("sms", 0.25)]
}

SCAMTYPES_SEARCH_MAPPING = {
    "Impersonation Scam": [("pretend", 0.5), ("government", 0.05), ("friend", 0.05), ("fake", 0.075), ("impersonate", 0.4)],
    "Phishing Scam": [("fake", 0.075), ("link", 0.2), ("email", 0.1), ("message", 0.1)],
    "Job Scam": [("job", 0.5), ("hire", 0.25), ("hiring", 0.25)],
    "Investment Scam": [("invest", 0.5), ("stock", 0.1), ("crypto", 0.1), ("bond", 0.1)],
    "Internet Love Scam": [("love", 0.5), ("loving", 0.2), ("girlfriend", 0.1), ("boyfriend", 0.1)],
    "Loan Scam": [("borrow", 0.3), ("loan", 0.5)],
    "Home/Room Rental Scam": [("rent", 0.4), ("room", 0.01)],
    "Software Update Scam": [("hack", 0.4)]
}

def _GetWeightMap(description: str, searchMap: dict) -> WeightMap:
    description = description.lower()
    weightMap = WeightMap()

    for platform in searchMap:
        # For each keyword to find
        for keywordMapping in searchMap[platform]:
            firstOccurance = description.find(keywordMapping[0])
            counts = description.count(keywordMapping[0])

            # If there is an occurance
            if firstOccurance >= 0:
                # Determine weight by occurance location and counts.
                lerpVal = firstOccurance / len(description)
                weightVal = Lerp(0.001, keywordMapping[1], lerpVal) + ((counts / 10.0) * keywordMapping[1])
                weightMap.AddValueToWeight(platform, weightVal)

    return weightMap

def DeterminePlatform(description: str) -> str:
    """
    Determine the platform the scam was conducted on from the description.
    """
    weightMap = _GetWeightMap(description, PLATFORM_SEARCH_MAPPING)

    # Find keyword with highest weight.
    result = weightMap.DetermineHighestWeight()
    if result == None:
        return "Unknown"
    return result

def DetermineScamTypes(description: str) -> list:
    weightMap = _GetWeightMap(description, SCAMTYPES_SEARCH_MAPPING)

    result = weightMap.GetHighestInRange(0.2)
    if len(result) == 0:
        result = ["Unknown"]
    return result