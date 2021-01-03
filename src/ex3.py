#!/usr/bin/env python3

# Author: Marek Filip <wecros|xfilip46>
# Date: 2020/12/27

import sys
import wave

import matplotlib.pyplot as plt
import numpy as np

from sklearn.preprocessing import minmax_scale
from lib import open_wave, centralize_signal, normalize_signal, \
                get_signal_frames, ms2sample, SAMPLE_RATE, \
                get_similar_subsignal, OUTPUT_PATH, save_figure, \
                get_tones_1s


def plot(on, off, save):
    """Plot one frame of the maskon/maskoff signals."""
    fig, (ax_on, ax_off) = plt.subplots(2, constrained_layout=True)
    fig.set_size_inches(8.0, 6.0)
    fig.canvas.set_window_title('Excercise 3')

    time = np.linspace(0, on.size / SAMPLE_RATE, num=on.size)

    ax_on.plot(time, on, 'tab:green')
    ax_off.plot(time, off, 'tab:red')

    ax_on.set_title('20ms of the mask-on tone')
    ax_on.set_xlabel('time [s]')
    ax_on.set_ylabel('y')
    ax_on.set_ylim(-1, 1)

    ax_off.set_title('20ms of the mask-off tone')
    ax_off.set_xlabel('time [s]')
    ax_off.set_ylabel('y')
    ax_off.set_ylim(-1, 1)

    if save:
        save_figure(fig, 'ex3')
    else:
        plt.show()


def output():
    """Return two frames of the maskon/maskoff tones."""
    # Get the maskon/maskoff 1s tones
    maskon, maskoff = get_tones_1s()

    maskon_center = centralize_signal(maskon)
    maskoff_center = centralize_signal(maskoff)
    maskon_normal = normalize_signal(maskon_center)
    maskoff_normal = normalize_signal(maskoff_center)

    maskon_frames = get_signal_frames(maskon_normal)
    maskoff_frames = get_signal_frames(maskoff_normal)
    # Remove the last frame containing only half of the needed values.
    maskon_frames.pop()
    maskoff_frames.pop()

    return (maskon_frames, maskoff_frames)


def main(save=False):
    maskon_frames, maskoff_frames = output()
    plot(maskon_frames[0], maskoff_frames[16], save)


if __name__ == '__main__':
    main()
