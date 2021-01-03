#!/usr/bin/env python3

# Author: Marek Filip <wecros|xfilip46>
# Date: 2020/01/03

import sys
import wave

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal

from lib import clip_centre, SAMPLE_RATE, OUTPUT_PATH, auto_correlate, \
                save_figure, compute_log_spectogram, N

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
    """
    Return the frequency characteristic filter tuple.

    1st - output used for further excercises
    2nd - output used for plotting
    """
    maskon_frames, maskoff_frames = ex3.output()

    # Get the maskon and maskoff DFTs
    maskon_dfts = np.fft.fft(maskon_frames, n=N)
    maskoff_dfts = np.fft.fft(maskoff_frames, n=N)

    fraction = maskon_dfts / maskoff_dfts

    # Make the values absolute
    fraction_abs = np.abs(fraction)
    fraction_plot = compute_log_spectogram(fraction)
    return [np.mean([frame[i] for frame in fraction_abs]) for i in range(N)], \
           [np.mean([frame[i] for frame in fraction_plot]) for i in range(N)]


def main(save=False):
    _, freqz_char_filter = output()
    plot(freqz_char_filter[:N//2], save)


if __name__ == '__main__':
    main()
