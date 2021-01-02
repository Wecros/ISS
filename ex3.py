#!/usr/bin/env python

# Author: Marek Filip <wecros|xfilip46>
# Date: 2020/12/27

import sys
import wave

import matplotlib.pyplot as plt
import numpy as np

from sklearn.preprocessing import minmax_scale
from lib import open_wave, centralize_signal, normalize_signal, \
                get_signal_frames, ms2sample, SAMPLE_RATE, \
                get_similar_subsignal, OUTPUT_PATH


def save_figure(fig):
    fig.savefig(OUTPUT_PATH + 'ex3.png')
    fig.savefig(OUTPUT_PATH + 'ex3-transparent.png', transparent=True)
    fig.savefig(OUTPUT_PATH + 'ex3.pdf')


def plot(on, off, save):
    """Plot one frame of the maskon/maskoff signals."""
    fig, (ax_on, ax_off) = plt.subplots(2, constrained_layout=True)
    fig.set_size_inches(8.0, 6.0)
    fig.canvas.set_window_title('Excercise 3')

    time = np.linspace(0, on.size / SAMPLE_RATE, num=on.size)

    ax_on.plot(time, on, 'tab:green')
    ax_off.plot(time, off, 'tab:red')

    ax_on.set_title('20ms of the maskon tone')
    ax_on.set_xlabel('time [s]')
    ax_on.set_ylabel('y')
    ax_on.set_ylim(-1, 1)

    ax_off.set_title('20ms of the maskoff tone')
    ax_off.set_xlabel('time [s]')
    ax_off.set_ylabel('y')
    ax_off.set_ylim(-1, 1)

    if save:
        save_figure(fig)
    else:
        plt.show()


def output():
    """Return two frames of the maskon/maskoff tones."""
    # Chosen 1000ms part of maskon_tone
    # maskon_wav: wave.Wave_read = open_wave('maskon_tone_1s.wav', 'rb')
    maskon_wav: wave.Wave_read = open_wave('maskon_tone.wav', 'rb')
    # The whole recording of maskoff_tone
    maskoff_wav: wave.Wave_read = open_wave('maskoff_tone.wav', 'rb')
    maskon_frames: bytes = maskon_wav.readframes(-1)
    maskoff_frames: bytes = maskoff_wav.readframes(-1)
    maskon_wav.close()
    maskoff_wav.close()

    maskon: np.ndarray = np.frombuffer(maskon_frames, dtype=np.int16)
    maskoff: np.ndarray = np.frombuffer(maskoff_frames, dtype=np.int16)

    # Cut the maskon sound to 1s - 16,000 samples
    maskon = maskon[200:16200]
    # Get the part of the maskoff_tone that is most similar to the 1s of maskon
    maskoff = get_similar_subsignal(maskon, maskoff)


    print(len(maskon), len(maskoff))

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
