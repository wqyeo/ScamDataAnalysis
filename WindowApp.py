import PySimpleGUI as sg
from Core.Async.AppTaskManager import AppTaskManager
from Core.Async.TaskThread import TaskThread

class WindowApp:
    """
    For inheritance by application windows.
    """
    def __init__(self, mainAsyncLoop, window, viewModel, onAppCloseEvent) -> None:
        self.window = window
        self.isOpen = True
        self.viewModels = viewModel
        self.asyncLoop = mainAsyncLoop
        self.asyncTaskManager = AppTaskManager(self)
        self._onAppCloseEvent = onAppCloseEvent

    def Update(self) -> None:
        event, value = self.window.read(timeout=10)

        if event == sg.WINDOW_CLOSED:
            self._onAppCloseEvent(self)
            return None
        # TODO: See if it possible to update the respective view-model
        # based on the current viewed Tab.
        for viewModel in self.viewModels:
            viewModel.Update(event, value)

    def CloseApp(self):
        self.isOpen = False

    def TryAddTask(self, task: TaskThread) -> bool:
        """
        Try to add a task to the app's async task pool.

        Return false if the task already exists.
        """
        if self.asyncTaskManager.TaskExists(task):
            return False
        self.asyncTaskManager.AddTask(task)
        return True
