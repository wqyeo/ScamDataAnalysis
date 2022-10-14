class WeightMap:
    def __init__(self) -> None:
        self._weights = {}

    def AddValueToWeight(self, weightName: str, value: float) -> None:
        if weightName in self._weights:
            self._weights[weightName] += value
        else:
            self._weights[weightName] = value

    def DetermineHighestWeight(self) -> str:
        currHighest = 0.0
        result = None
        for weight in self._weights:
            if self._weights[weight] > currHighest:
                result = weight
                currHighest = self._weights[weight]
        return result