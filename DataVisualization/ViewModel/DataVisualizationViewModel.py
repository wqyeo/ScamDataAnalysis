import numpy as np
import matplotlib.figure
import matplotlib.pyplot as plt

from DataVisualization.Model.DataVisualizationModel import DataVisualizationModel


class DataVisualizationViewModel:
    def __init__(self, appRef) -> None:
        self.appRef = appRef
        self.model = DataVisualizationModel(self)

    def create_figure(self) -> None:
        fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
        fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
        t = np.arange(0, 3, .01)
        fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

    def create_pie(self) -> None:
        # ------------------------------- START OF YOUR MATPLOTLIB CODE -------------------------------
        labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
        sizes = [15, 30, 45, 10]
        explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.