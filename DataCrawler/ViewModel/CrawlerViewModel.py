import PySimpleGUI as sg
from DataCrawler.View.CrawlerView import *

class CrawlerViewModel:
    def __init__(self, appRef) -> None:
        self.appRef = appRef
        pass

    def Update(self, window) -> None:
        event, value = window.read()
        if event == sg.WINDOW_CLOSED:
            self.appRef.CloseApp()
        elif event == START_CRAWL:
            self.StartCrawl(window)

    def StartCrawl(self, window) -> None:
        file_path = window[SAVE_FOLDER_KEY].get()

        if not file_path.strip():
            self.ShowUserMessage("File Path should not be empty", window)
            return None
        else:
            self.ShowUserMessage("", window)

    def ShowUserMessage(self, msg: str, window) -> None:
        """
        Show a message to the user.
        (Commonly used to show error or log.)
        """
        window[CRAWLER_USER_LOG_MESSAGE].update(msg)