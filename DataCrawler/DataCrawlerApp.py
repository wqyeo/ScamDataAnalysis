import PySimpleGUI as sg

class DataCrawlerApp:
    def __init__(self) -> None:
        self.window = sg.Window(title = "Data Crawler", layout=[[]], margins=(50, 20))
        self.isOpen = True
        pass

    def Update(self) -> None:
        event, value = self.window.read()
        if event == sg.WINDOW_CLOSED:
            self.isOpen = False