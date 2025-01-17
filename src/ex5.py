#!/usr/bin/env python3

# Author: Marek Filip <wecros|xfilip46>
# Date: 2020/01/02

import sys
import wave

import matplotlib.pyplot as plt
import numpy as np

from sklearn.preprocessing import minmax_scale
from lib import clip_centre, SAMPLE_RATE, OUTPUT_PATH, auto_correlate, \
                save_figure, compute_log_spectogram, N

import ex3


def plot(maskon, maskoff, save):
    """Plot the spectograms of the maskon/maskoff frames."""
    fig, axes = plt.subplots(2, constrained_layout=True)
    fig.set_size_inches(8.0, 6.0)
    fig.canvas.set_window_title('Excercise 5')

    ax_on, ax_off = axes

    im_on = ax_on.imshow(maskon, origin='lower', aspect='auto', extent = [0 , 1.0, 0 , 8000])
    fig.colorbar(im_on, ax=ax_on)
    im_off = ax_off.imshow(maskoff, origin='lower', aspect='auto', extent = [0 , 1.0, 0 , 8000])
    fig.colorbar(im_off, ax=ax_off)

    ax_on.set_title('Mask-on spectogram')
    ax_off.set_title('Mask-off spectogram')

    for ax in axes:
        ax.set_xlabel('time [s]')
        ax.set_ylabel('frequency')

    if save:
        save_figure(fig, 'ex5')
    else:
        plt.show()


def main(save=False):
    maskon_frames, maskoff_frames = ex3.output()

    maskon_dfts = np.fft.fft(maskon_frames, n=N)
    maskoff_dfts = np.fft.fft(maskoff_frames, n=N)

    maskon_spectogram = compute_log_spectogram(maskon_dfts)
    maskoff_spectogram = compute_log_spectogram(maskoff_dfts)
    maskon_spectogram = maskon_spectogram.transpose()
    maskoff_spectogram = maskoff_spectogram.transpose()

    plot(maskon_spectogram[:N//2], maskoff_spectogram[:N//2], save)


if __name__ == '__main__':
    main()
