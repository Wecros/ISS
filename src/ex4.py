#!/usr/bin/env python3

# Author: Marek Filip <wecros|xfilip46>
# Date: 2020/12/27

import sys
import wave

import matplotlib.pyplot as plt
import numpy as np

from sklearn.preprocessing import minmax_scale
from lib import clip_centre, SAMPLE_RATE, OUTPUT_PATH, auto_correlate, \
                save_figure

import ex3


def plot(frame, clipped, auto, lag, threshold, freq, save):
    """
    Plot the maskon clip and autocorrelation, plot the frequencies of
    maskon and maskoff signals.
    """
    fig, axes = plt.subplots(4, constrained_layout=True)
    fig.set_size_inches(8.0, 8.0)
    fig.canvas.set_window_title('Excercise 4')

    ax_frame, ax_clipped, ax_auto, ax_freq = axes

    time = np.linspace(0, frame.size / SAMPLE_RATE, num=frame.size)
    for ax in axes:
        ax.set_xlabel('time [s]')
        ax.set_ylabel('y')


    ax_frame.plot(time, frame)
    ax_clipped.plot(time, clipped)

    ax_auto.plot(auto)
    ax_auto.axvline(threshold, color='black', label='Threshold')
    ax_auto.stem([lag[0]], [lag[1]], linefmt='r-', basefmt=None, label='Lag')

    ax_freq.plot(freq[0], 'g-', label='mask-on')
    ax_freq.plot(freq[1], 'r-', label='mask-off')

    ax_auto.legend(loc=1)
    ax_freq.legend(loc=0)

    ax_frame.set_title('Maskon frame')
    ax_clipped.set_title('Central clipping with 70%')
    ax_auto.set_title('Autocorrelation')
    ax_freq.set_title('Primary frequencies of frames')

    ax_auto.set_xlabel('frames')
    ax_freq.set_xlabel('frames')

    ax_freq.set_ylabel('f0')

    if save:
        save_figure(fig, 'ex4')
    else:
        plt.show()


def get_frequency(frame):
    """Get frequency of lag from certain frame."""
    frame = clip_centre(frame)
    frame = auto_correlate(frame)
    threshold: int = SAMPLE_RATE // 500
    lag = frame[threshold:].argmax()
    frequency = SAMPLE_RATE / lag
    return frequency


def main(save=False):
    maskon_frames, maskoff_frames = ex3.output()

    maskon = maskon_frames[0]
    # Apply centre clipping with 70% threshold
    maskon_clip = clip_centre(maskon)
    # Apply autocorrelation
    maskon_auto  = auto_correlate(maskon_clip)

    # Find the index of maximum coeficient - lag 
    # The beginning part of the autocorrelation will always be the highest,
    # therefore we need to pick a beginning threshold (e.g. 500 Hz)
    threshold: int = SAMPLE_RATE // 500
    maskon_lag = [maskon_auto[threshold:].argmax() + threshold, maskon_auto[threshold:].max()]

    maskon_frequencies = [get_frequency(frame) for frame in maskon_frames]
    maskoff_frequencies = [get_frequency(frame) for frame in maskoff_frames]

    frequencies = [maskon_frequencies, maskoff_frequencies]
    plot(maskon, maskon_clip, maskon_auto, maskon_lag, threshold, frequencies, save)


if __name__ == '__main__':
    main()
