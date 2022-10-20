from operator import truediv
import PySimpleGUI as sg
from Core.Async.AppTaskManager import AppTaskManager
from Core.Async.TaskThread import TaskThread

class WindowApp:
    """
    For inheritance by application windows.
    """
    def __init__(self, mainAsyncLoop, window: sg.Window, viewModel) -> None:
        self.window = window
        self.isOpen = True
        self.viewModels = viewModel
        self.asyncLoop = mainAsyncLoop
        self.asyncTaskManager = AppTaskManager(self)

    def Update(self) -> None:
        event, value = self.window.read(timeout=10)

        if event == sg.WINDOW_CLOSED or event == sg.WIN_CLOSED:
            self.asyncTaskManager.RemoveIdleTasks()
            if len(self.asyncTaskManager.currentTasks) > 0:
                    self.asyncTaskManager.EndAllTask()
            self.CloseApp()
            return None

        for viewModel in self.viewModels:
            viewModel.Update(event, value)

    def CloseApp(self):
        self.isOpen = False
        self.window.close()

    def TryAddTask(self, task: TaskThread) -> bool:
        """
        Try to add a task to the app's async task pool.

        Return false if the task already exists.
        """
        if self.asyncTaskManager.TaskExists(task):
            return False
        self.asyncTaskManager.AddTask(task)
        return True
