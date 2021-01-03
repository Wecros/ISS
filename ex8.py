#!/usr/bin/env python

# Author: Marek Filip <wecros|xfilip46>
# Date: 2020/01/03

import sys
import wave

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal

from lib import open_wave, centralize_signal, normalize_signal, \
                get_signal_frames, ms2sample, SAMPLE_RATE, \
                get_similar_subsignal, OUTPUT_PATH, save_figure

import ex3


def plot(on, off, sim, save):
    """Plot the frequency characterstic filter of the maskon/maskoff tones."""
    fig, axes = plt.subplots(3, constrained_layout=True)
    fig.set_size_inches(8.0, 6.0)
    fig.canvas.set_window_title('Excercise 6')

    ax_off, ax_on, ax_sim = axes

    # time = np.linspace(0, on.size[0] / SAMPLE_RATE, num=on.size)
    ax_off.plot(off, c='red')
    ax_on.plot(on, c='green')
    ax_sim.plot(on, c='yellow')

    ax_off.set_title('Maskoff sentence')
    ax_on.set_title('Maskon sentence')
    ax_sim.set_title('Simulated maskon sentence')

    for ax in axes:
        ax.set_xlabel('time [s]')
        ax.set_ylabel('y')
        ax.set_ylim(-1, 1)

    if save:
        save_figure(fig, 'ex8')
    else:
        plt.show()


def main(save=False):
    # Read the sentence recordings
    maskonsen_wav: wave.Wave_read = open_wave('maskon_sentence.wav', 'rb')
    maskoffsen_wav: wave.Wave_read = open_wave('maskoff_sentence.wav', 'rb')
    maskonsen_frames: bytes = maskonsen_wav.readframes(-1)
    maskoffsen_frames: bytes = maskoffsen_wav.readframes(-1)
    maskonsen_wav.close()
    maskoffsen_wav.close()

    # Get the maskon/maskoff 1s tones (frames)
    maskon_frames, maskoff_frames = ex3.output()

    # Get the maskonsen/maskoffsen arrays 
    maskonsen: np.ndarray = np.frombuffer(maskonsen_frames, dtype=np.int16)
    maskoffsen: np.ndarray = np.frombuffer(maskoffsen_frames, dtype=np.int16)

    # Normalize the signals and get frames
    maskonsen_center = centralize_signal(maskonsen)
    maskoffsen_center = centralize_signal(maskoffsen)
    maskonsen_normal = normalize_signal(maskonsen_center)
    maskoffsen_normal = normalize_signal(maskoffsen_center)

    maskonsen_frames = get_signal_frames(maskonsen_normal)
    maskoffsen_frames = get_signal_frames(maskoffsen_normal)

    plot(maskonsen_normal, maskoffsen_normal, save)


if __name__ == '__main__':
    main()
