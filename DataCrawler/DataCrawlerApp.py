import PySimpleGUI as sg

from DataCrawler.View.CrawlerView import *

class DataCrawlerApp:
    def __init__(self) -> None:
        self.window = sg.Window(title = "Data Crawler", layout= CreateCrawlerViewLayout(), margins=(50, 20))
        self.isOpen = True
        pass

    def Update(self) -> None:
        event, value = self.window.read()
        if event == sg.WINDOW_CLOSED:
            self.isOpen = False
        elif event == START_CRAWL:
            self.StartCrawl()

    def ShowUserMessage(self, msg: str) -> None:
        """
        Show a message to the user.
        (Commonly used to show error or log.)
        """
        self.window[CRAWLER_USER_LOG_MESSAGE].update(msg)

    def StartCrawl(self) -> None:
        file_path = self.window[SAVE_FOLDER_KEY].get()

        if not file_path.strip():
            self.ShowUserMessage("File Path should not be empty")
            return None
        else:
            self.ShowUserMessage("")