import PySimpleGUI as sg


#region NOTE: Keys
TARGET_CRAWL_DATA_KEY = "TARGET_CRAWL_DATA_KEY"

CRAWLER_USER_LOG_KEY = "DEEP_CRAWLER_USER_LOG_MESSAGE"
LOADING_BAR_KEY = "DEEP_LOADING_BAR_KEY"
#endregion

#region NOTE: Events (Button names, etc)
START_CRAWL_EVENT = "Deep Crawl"
#endregion 

def CreateDeepCrawlerViewLayout():

    _CRAWL_DATA_SELECTION =[
        [sg.Text("Target JSON Data File\n(Data will be saved in the same location): ")],
        [sg.In(key=TARGET_CRAWL_DATA_KEY, readonly=True)],
        [sg.FileBrowse(target=TARGET_CRAWL_DATA_KEY, file_types=(("JSON files", "*.json"),))]
    ]

    return [
        [sg.Column(_CRAWL_DATA_SELECTION)],
        [sg.HorizontalSeparator()],
        [sg.Text("", key=CRAWLER_USER_LOG_KEY)],
        [sg.Button(START_CRAWL_EVENT)],
        [sg.ProgressBar(max_value= 100,  key = LOADING_BAR_KEY, orientation="h", size=(20, 20))]
    ]