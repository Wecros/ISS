#!/usr/bin/env python

# Author: Marek Filip <wecros|xfilip46>
# Date: 2020/01/03

import sys
import wave

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal

from lib import clip_centre, SAMPLE_RATE, OUTPUT_PATH, auto_correlate, \
                save_figure

import ex3


def plot(char, save):
    """Plot the frequency characterstic filter of the maskon/maskoff tones."""
    fig, ax_char = plt.subplots(1, constrained_layout=True)
    fig.set_size_inches(8.0, 6.0)
    fig.canvas.set_window_title('Excercise 6')

    ax_char.plot(char)

    ax_char.set_title('Frequency characteristic filter')
    ax_char.set_xlabel('Spectrum of frames')
    ax_char.set_ylabel('y')

    if save:
        save_figure(fig, 'ex6')
    else:
        plt.show()


def output():
    """Return the frequency characteristic filter."""
    maskon_frames, maskoff_frames = ex3.output()

    # Get the maskon and maskoff DFTs
    N = 1024
    maskon_dfts = np.fft.fft(maskon_frames, n=N)
    maskoff_dfts = np.fft.fft(maskoff_frames, n=N)

    fraction = maskon_dfts / maskoff_dfts

    # Same formula as in ex5
    compute_values = lambda arr: 10 * np.log10(abs(arr) ** 2)

    # Make the values absolute
    fraction_abs = compute_values(fraction)
    return [np.mean([frame[i] for frame in fraction_abs]) for i in range(N//2)]


def main(save=False):
    freqz_char_filter = output()
    plot(freqz_char_filter, save)


if __name__ == '__main__':
    main()
