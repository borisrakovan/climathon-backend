import numpy as np
import matplotlib.pyplot as plt


def gaussian_kernel(l, sig=1.):
    """\
    creates gaussian kernel with side length `l` and a sigma of `sig`
    """
    ax = np.linspace(-(l - 1) / 2., (l - 1) / 2., l)
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sig))
    kernel = np.outer(gauss, gauss)
    return kernel / np.sum(kernel)


def minmax_normalize(arr, min=None, max=None):
    if min is None:
        min = np.min(arr)
    if max is None:
        max = np.max(arr)

    return (arr - np.min(arr)) / (max - min)


def show_heatmap(arr):
    plt.imshow(arr, cmap='hot', interpolation='nearest')
    plt.show()
