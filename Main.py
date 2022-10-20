from asyncio import AbstractEventLoop
import PySimpleGUI as sg

from Core.Async.AsyncThread import *
from DataCrawler.DataCrawlerApp import *
from DataVisualization.DataVisualizationApp import DataVisualizationApp


def _CreateMainWindow():
    WINDOW_TITLE = "Scam Data Analysis"
    WINDOW_MARGIN = (50, 25)
    WINDOW_LAYOUT = [
        [sg.Text("Select App: ")],
        [sg.Button("Crawler"), sg.Button("Anaylzer")],
        [sg.Text("", key="Error_MSG")]
    ]

    return sg.Window(title=WINDOW_TITLE, layout=WINDOW_LAYOUT, margins=WINDOW_MARGIN)


def _RunMainWindow(mainThread: Thread, mainAsyncLoop: AbstractEventLoop) -> None:
    appWindow = _CreateMainWindow()

    while True:
        event, value = appWindow.read(timeout=10)
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Crawler":
            appWindow.close()
            _RunApplication(DataCrawlerApp(mainAsyncLoop))
            appWindow = _CreateMainWindow()
        elif event == "Anaylzer":
            appWindow.close()
            _RunApplication(DataVisualizationApp(mainAsyncLoop))
            appWindow = _CreateMainWindow()

    appWindow.close()

def _RunApplication(app) -> None:
    while app.isOpen:
        app.Update()


_mainAsyncThread = StartAsyncLoop()
_RunMainWindow(_mainAsyncThread[0], _mainAsyncThread[1])