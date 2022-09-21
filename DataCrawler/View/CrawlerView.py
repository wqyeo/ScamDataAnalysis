import PySimpleGUI as sg

#region NOTE: Consts
_CRAWL_SITE_OPTIONS = [
    "ScamAlert - Stories",
    "ScamAlert - News"
]
#endregion

#region NOTE: Keys
TARGET_CRAWL_SITE_KEY = "TARGET_CRAWL_SITE_KEY"
SAVE_FOLDER_KEY = "SAVE_FOLDER_KEY"
RECURSIVE_CRAWL_TIMES_KEY = "RECURSIVE_CRAWL_TIMES_KEY"

CRAWLER_USER_LOG_KEY = "CRAWLER_USER_LOG_MESSAGE"
LOADING_BAR_KEY = "LOADING_BAR_KEY"
#endregion

#region NOTE: Events (Button names, etc)
START_CRAWL = "Crawl!"
#endregion 

def CreateCrawlerViewLayout():
    # NOTE: Minor layouts to be merged together to form the full layout
    _CRAWL_SITE_SELECTOR = [sg.Text("Select Site to Crawl: "), sg.Combo(_CRAWL_SITE_OPTIONS, key= TARGET_CRAWL_SITE_KEY, readonly= True, default_value=_CRAWL_SITE_OPTIONS[0])],

    _RECURSIVE_CRAWL_SELECTOR = [sg.Text('No of pages to crawl through: '), sg.Spin([i for i in range(1,101)], initial_value=10, key=RECURSIVE_CRAWL_TIMES_KEY, readonly=True)]

    _SAVE_DESTINATION_SELECTION =[
        [sg.Text("Target Folder (data will be saved here): ")],
        [sg.In(key=SAVE_FOLDER_KEY, readonly=True)],
        [sg.FolderBrowse(target=SAVE_FOLDER_KEY)]
    ]

    return [
        _CRAWL_SITE_SELECTOR,
        _RECURSIVE_CRAWL_SELECTOR,
        [sg.Column(_SAVE_DESTINATION_SELECTION)],
        [sg.HorizontalSeparator()],
        [sg.Text("", key=CRAWLER_USER_LOG_KEY)],
        [sg.Button(START_CRAWL)],
        [sg.ProgressBar(max_value= 100,  key = LOADING_BAR_KEY, orientation="h", size=(20, 20))]
    ]