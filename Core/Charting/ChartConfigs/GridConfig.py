from Core.Charting.ChartConfigs.TargetAxis import TargetAxis
from Core.Charting.ChartConfigs.TargetGrid import TargetGrid

class GridConfig:
    def __init__(self, targetAxis : TargetAxis = TargetAxis.BOTH, targetGrid : TargetGrid = TargetGrid.MAJOR,linestyle :str = '--', linewidth : float = 0.5):
        self._targetAxis = targetAxis
        self._targetGrid = targetGrid
        self.linestyle = linestyle
        self.linewidth = linewidth

    def GetTargetAxis(self):
        return self._targetAxis.name.lower()
    
    def GetTargetGrid(self):
        return self._targetGrid.name.lower()