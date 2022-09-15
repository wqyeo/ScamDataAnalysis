import PySimpleGUI as sg

from DataCrawler.DataCrawlerApp import DataCrawlerApp

def CreateMainWindow():
    WINDOW_TITLE = "Scam Data Analysis"
    WINDOW_MARGIN = (50, 25)
    WINDOW_LAYOUT = [
        [sg.Text("Select App: ")],
        [sg.Button("Crawler"), sg.Button("Anaylzer")],
        [sg.Text("", key="Error_MSG")]
    ]

    return sg.Window(title= WINDOW_TITLE, layout = WINDOW_LAYOUT, margins= WINDOW_MARGIN)

def RunMainWindow() -> None:
    appWindow = CreateMainWindow()

    while True:
        event, value = appWindow.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Crawler":
            # TODO: Open crawler
            appWindow.close()
            RunApplication(DataCrawlerApp())
            appWindow = CreateMainWindow()
        elif event == "Anaylzer":
            appWindow["Error_MSG"].update("Analyzer Not Implemented yet")
            pass

    appWindow.close()

def RunApplication(app) -> None:
    while app.isOpen:
        app.Update()

RunMainWindow()