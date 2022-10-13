from Core.Charting.Charts.VisualChart import VisualChart

class PieChart(VisualChart):
    def __init__(self, title, data: list, othersCutOff: int = 3):
        """
        A Pie Chart

        Parameters
        ------------------------
        **others_cut_off**
        Anything below this value will be categorised into 'others' section instead.
        """
        self.othersCutOff = othersCutOff
        super().__init__(title)
