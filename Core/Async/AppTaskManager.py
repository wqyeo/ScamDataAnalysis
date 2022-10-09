from Core.Async.TaskThread import *
from Core.Logging.LogSeverity import LogSeverity
from Core.Logging.Logger import Log

class AppTaskManager:
    def __init__(self, appRef) -> None:
        self._appRef = appRef
        self.currentTasks = []
        pass

    def TaskExists(self, task: TaskThread) -> bool:
        for thread in self.currentTasks:
            if thread.name == task.name:
                return True
        return False

    def AddTask(self, task: TaskThread) -> None:
        if self.TaskExists(task):
            Log("Thread Task already Exists.", "Thread task already exists for {}, but we are still adding it.".format(task.name), LogSeverity.WARNING)
        self.currentTasks.append(task)

    def RemoveIdleTasks(self) -> None:
        # Remove all tasks in list that is not running.
        self.currentTasks = [task for task in self.currentTasks if task.isRunning]

