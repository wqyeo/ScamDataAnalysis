from Core.Util import GetFileNameFromPath

class VisualizationViewModel:
    """
    Used as a parent/abstract class to be
    """
    def __init__(self, appRef, model, imageKey, userMessageKey, imageSelectionKey) -> None:
        self.appRef = appRef
        self.model = model

        self._appWindow = appRef.window
        self._figurePathBindings = {}
        self._lastFigure = ""

        # For 'animating' a loading message
        self._analyzeThread = None
        self._userMessageCycle = 1
        self._cycle = 0

        self._userMessageKey = userMessageKey
        self._imageKey = imageKey
        self._imageSelectionKey = imageSelectionKey

    def Update(self, event, value):
        pass

    def SetFigurePaths(self, figurePaths: str) -> None:
#region Local_Function
        def BindFigurePaths(plotPaths: list) -> None:
            self._figurePathBindings = {}
            for path in plotPaths:
                name = GetFileNameFromPath(path)
                self._figurePathBindings[name.replace("_", " ")] = path
#endregion

        if figurePaths != None:
            BindFigurePaths(figurePaths)
            figureNames = list(self._figurePathBindings.keys())
            self._UpdateFigure(figureNames[0], True)
            self._appWindow[self._imageSelectionKey].update(values= figureNames, visible=True)
            self.ShowUserMessage("Analyzed!")
        else:
            self.ShowUserMessage("Analyze failed or cancelled.")

    def _UpdateFigure(self, figName, ignoreLast = False) -> None:
        if figName in self._figurePathBindings:
            if figName != self._lastFigure and not ignoreLast:
                self._lastFigure = figName
                self._appWindow[self._imageKey].update(self._figurePathBindings[figName])
            elif ignoreLast:
                self._lastFigure = figName
                self._appWindow[self._imageKey].update(self._figurePathBindings[figName])

    def ShowUserMessage(self, message: str) -> None:
        self._appWindow[self._userMessageKey].update(message)

    def FreeAppThread(self):
        self.appRef.asyncTaskManager.RemoveIdleTasks()