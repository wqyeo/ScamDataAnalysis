class WeightMap:
    """
    Represents a non-balanced dummy weightmap
    """
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

    def GetHighestInRange(self, range: float) -> list:
        """
        Return list of weights within the range of the highest weight.
        """
        sortedWeights = {key: val for key, val in sorted(self._weights.items(), key = lambda ele: ele[1], reverse = True)}

        result = []
        currHighest = 0.0
        highest = None
        for weight in sortedWeights:
            if highest == None:
                highest = weight
                currHighest = self._weights[weight]
                result.append(highest)
                continue

            if self._weights[weight] + range >= currHighest:
                result.append(highest)
            else:
                break
        return result