import numpy as np
import matplotlib.pyplot as plt

mir_len_x = 0.14
mir_len_y = 0.14
space = 0.002
num_x = 11
num_y = 7


def create_coords(dim, space, num_elements):
    step = dim + space
    coords = np.arange(0, num_elements) * step
    return coords - coords[-1] / 2  # center coords at rectangle center


def plot_coords():
    xx, yy = np.meshgrid(centered_x, centered_y)
    plt.plot(xx, yy, marker=',', color='k', linestyle='none')
    plt.plot(0, 0, 'ro')


centered_x = create_coords(mir_len_x, space, num_x)
centered_y = create_coords(mir_len_y, space, num_y)

# plot_coords()
