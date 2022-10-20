class CrawlViewModel:
    def __init__(self, appRef, model, userLogKey, loadingBarKey) -> None:
        self.appRef = appRef
        self.model = model

        self._userLogKey = userLogKey
        self._loadingBarKey = loadingBarKey

    def Update(self, event, value) -> None:
        pass

    def ShowUserMessage(self, message) -> None:
        """
        Show a message to the user.
        (Commonly used to show error or log.)
        """
        self.appRef.window[self._userLogKey].update(message)

    def UpdateLoadingBar(self, percentValue: int) -> None:
        self.appRef.window[self._loadingBarKey].update(percentValue)

    def FreeAppThread(self):
        self.appRef.asyncTaskManager.RemoveIdleTasks()