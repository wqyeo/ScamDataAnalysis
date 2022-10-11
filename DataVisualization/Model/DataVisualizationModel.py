from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io


class DataVisualizationModel:
    def __init__(self, viewModelRef) -> None:
        self.viewModelRef = viewModelRef
        pass

    def draw_figure(self, figure):
        plt.close('all')  # erases previously drawn plots
        canv = FigureCanvasAgg(figure)
        buf = io.BytesIO()
        canv.print_figure(buf, format='png')
        if buf is None:
            return None
        buf.seek(0)
        self.update(data=buf.read())
        return canv
