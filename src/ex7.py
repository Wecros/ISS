#!/usr/bin/env python

# Author: Marek Filip <wecros|xfilip46>
# Date: 2020/01/03

import sys
import wave

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal

from lib import clip_centre, SAMPLE_RATE, OUTPUT_PATH, auto_correlate, \
                save_figure, compute_log_spectogram

import ex6


def plot(char, save):
    """Plot the frequency characterstic filter of the maskon/maskoff tones."""
    fig, ax_char = plt.subplots(1, constrained_layout=True)
    fig.set_size_inches(8.0, 6.0)
    fig.canvas.set_window_title('Excercise 7')

    ax_char.plot(char)

    ax_char.set_title('Impulse latency')
    ax_char.set_xlabel('Spectrum of frames')
    ax_char.set_ylabel('y')

    if save:
        save_figure(fig, 'ex7')
    else:
        plt.show()


def output():
    """Return the frequency characteristic filter."""
    freqz_char_filter = ex6.output()
    # inv_fft = np.array(shape=(99, 1024), dtype=complex)
    N = 1024
    inv_fft = np.fft.ifft(freqz_char_filter, n=N)
    imp_lat = np.real(inv_fft)

    return imp_lat[:N//2]


def main(save=False):
    imp_lat = output()
    plot(imp_lat, save)


if __name__ == '__main__':
    main()
