#!/usr/bin/env python3

# Author: Marek Filip <wecros|xfilip46>
# Date: 2020/01/03

import sys
import wave

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal

from lib import open_wave, centralize_signal, normalize_signal, \
                get_signal_frames, ms2sample, SAMPLE_RATE, \
                get_similar_subsignal, OUTPUT_PATH, save_figure, \
                compute_log_spectogram, wave_write, get_tones

import ex7


def plot(on, off, sim, save):
    """Plot the frequency characterstic filter of the maskon/maskoff tones."""
    fig, axes = plt.subplots(4, constrained_layout=True)
    fig.set_size_inches(8.0, 8.0)
    fig.canvas.set_window_title('Excercise 6')

    ax_off, ax_on, ax_sim, ax_diff = axes

    off_time = np.linspace(0, off.size / SAMPLE_RATE, num=off.size)
    on_time = np.linspace(0, on.size / SAMPLE_RATE, num=on.size)
    sim_time = np.linspace(0, sim.size / SAMPLE_RATE, num=sim.size)

    ax_off.plot(off_time, off, c='red')
    ax_on.plot(on_time, on, c='green')
    ax_sim.plot(sim_time, sim)
    ax_diff.plot(sim_time, sim, label='simulated mask-on', alpha=0.9)
    ax_diff.plot(off_time, off, c='red', label='mask-off', alpha=0.85)
    ax_diff.legend(loc=4)

    ax_off.set_title('Mask-off sentence')
    ax_on.set_title('Mask-on sentence')
    ax_sim.set_title('Simulated mask-on sentence')
    ax_diff.set_title('Difference between mask-off and simulated mask-on')

    for ax in axes:
        ax.set_xlabel('time [s]')
        ax.set_ylabel('y')
        # ax.set_ylim(-1, 1)

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

    # Get the maskon/maskoff tones
    maskon, maskoff = get_tones()

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

    # Simulate the sentence and tone
    imp_lat = ex7.output()
    sim_sen = scipy.signal.lfilter(imp_lat, [1], maskoffsen)
    sim_tone = scipy.signal.lfilter(imp_lat, [1], maskoff)

    wave_write('sim_maskon_sentence.wav', sim_sen)
    wave_write('sim_maskon_tone.wav', sim_tone)

    plot(maskonsen, maskoffsen, sim_sen, save)


if __name__ == '__main__':
    main()
