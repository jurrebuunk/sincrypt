import matplotlib.pyplot as plt
from typing import List, Tuple
import numpy as np

def plot_sine_waves(
    waves: List[Tuple[float,float,float]],
    seed: float,
    encrypted_wave: np.ndarray = None,
    length: int = 50,
    smooth_factor: int = 20
):
    """
    Plot only the encrypted wave, smoothed via interpolation.
    """
    # Fine x-axis for smoothing
    x_fine = np.linspace(0, length-1, length * smooth_factor)

    fig, ax = plt.subplots()
    ax.set_facecolor("white")
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Plot encrypted wave (thick black) overlayed on same axes
    if encrypted_wave is not None:
        y_enc = np.interp(x_fine, np.arange(len(encrypted_wave)), encrypted_wave)
        ax.plot(x_fine, y_enc, color='black', linewidth=3, antialiased=True)

    plt.show()
