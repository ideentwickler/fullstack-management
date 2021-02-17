import base64
import matplotlib.pyplot as plt
from io import BytesIO


class CreatePlot:
    def __init__(self, labels, values, **kwargs):
        self.kwargs = kwargs
        self.values = values
        self.labels = labels

    def get_color(self, index: int):
        color: str = ''
        if 'colors' in self.kwargs:
            color = self.kwargs['colors'][index]
        return color

    def get_data(self):
        fig, ax = plt.subplots(figsize=(8, 3.4))

        if isinstance(self.values, list):
            ax.plot(self.labels, self.data)
        elif isinstance(self.values, dict):
            i = 0
            for key, value in self.values.items(): #for data in self.data.values():
                ax.plot(self.labels, value, label=key, color=self.get_color(index=i))
                i += 1
        plt.rcParams.update({'font.family': 'sans-serif'})

        plt.legend(loc='best')

        ax.set(xlabel='', ylabel='Auftragseingang',
               title='Performance Analyse')
        ax.grid()
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png', dpi=200)
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        plt.close()

        return encoded