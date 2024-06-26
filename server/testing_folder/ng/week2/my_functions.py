import numpy as np
import copy, math
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

dlblue = '#0096ff'
file_path = 'data'


class DataHandler:

    def __init__(self, filepath: str):
        self.filepath = filepath

    def load_data(self):
        """
            Load the data and returns the features and output
        """
        data: np.array = np.loadtxt(self.filepath, delimiter=",")
        print(data)
        X = data[:, :2]
        y = data[:, 2]
        return X, y

    def plt_house_x(self, f_wb=None, ax=None):
        X,y = self.load_data()
        if not ax:
            fig, ax = plt.subplot(1, 1)

        ax.scatter(X, y, marker="x", c="r", label="Actual Value")
        ax.set_title("House Pricing")
        ax.set_xlabel(f'Size (1000 sqft)')
        if f_wb is not None:
            ax.plot(X, f_wb, c = dlblue, label = "Our Prediction")
        ax.legend()

    def mk_cost_lines(self, w, b, ax):
        x, y = self.load_data()
        cstr = "cost = (1/2m)*1000*("
        ctot = 0
        label = 'cost per ponint'
        for p in zip(x, y):
            f_wb_p = w * p[0] + b
            c_p = ((f_wb_p - p[1])**2)/2
            c_p_text = c_p/1000
            ax.vlines(p[0], p[1], f_wb_p)




