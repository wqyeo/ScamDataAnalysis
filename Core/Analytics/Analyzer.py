import matplotlib.pyplot as plt

from Core.Database import Database
from Core.Logging.LogSeverity import LogSeverity
from Core.Logging.Logger import Log

class Analyzer:
    def __init__(self, filePath: str, outputPath: str) -> None:
        self.filePath = filePath
        self.outputPath = outputPath

    def AnalyzeData(self) -> bool:
#region Local_Functions
        def truncateKeys(datecount, length):
            return dict((k[6:length], v) for k, v in datecount.items())
#endregion

        jsonData = None
        try:
            jsonData = Database.OpenJsonData(self.filePath)

            # TODO: Allow loading from other data types
            if not ('Stories' in jsonData):
                raise Exception("JSON Format Invalid")
            jsonData = jsonData['Stories']
        except:
            Log("Error Convering Json File", "Error Converting JSON File from path {}.".format(self.filePath), LogSeverity.WARNING)
            return False

        dateData = []
        for i in jsonData:
            if 'Date' in i:
                dateData.append(i)

        dateCount = dict()
        for i in dateData:
            dateCount[i] = dateCount.get(i, 0) + 1
        dateCount = dict(sorted(dateCount.items()))

        shortendate = truncateKeys(dateCount, -4)

        # TODO: Find a way to output plot
        # Plotting
        xAxis = [key for key, value in shortendate.items()]
        yAxis = [value for key, value in shortendate.items()]
        plt.grid(True)

        ## LINE GRAPH ##
        plt.plot(xAxis, yAxis, color='maroon', marker='o')
        plt.xlabel('Date')
        plt.ylabel('Number of Scam Cases')

        ## BAR GRAPH ##
        # fig = plt.figure()
        # plt.bar(xAxis, yAxis, color='maroon')
        # plt.xlabel('Date')
        # plt.ylabel('Number of Scam Cases')

        plt.savefig(self.outputPath)
        return True