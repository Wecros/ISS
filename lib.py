# Author: Marek Filip <wecros|xfilip46>
# Date: 2020/12/27
# Details: Auxiliary functions used in other parts of the project.

import sys
import wave

import numpy as np

from sklearn.preprocessing import minmax_scale


# Constants
SAMPLE_RATE = 16000
AUDIO_PATH = 'audio/'
OUTPUT_PATH = 'output/'


# Function definitions
def open_wave(filename, mode):
    return wave.open(AUDIO_PATH + filename, mode=mode)


def centralize_signal(signal):
    """Return the centrilized signal."""
    centralized_signal = signal - signal.mean()
    return centralized_signal


def normalize_signal(signal):
    """Return the normalized signal with range [-1,1]."""
    norm = np.linalg.norm(signal)
    signal = signal - norm
    normalized_signal = minmax_scale(signal, feature_range=(-1, 1))
    return normalized_signal


def get_similar_subsignal(subsignal, signal, rate=SAMPLE_RATE):
    """
    Return the subpart of the signal that is most similar to the subsignal.
    """
    # cor = cross-corelation array of subsignal and signal
    cor = np.correlate(subsignal, signal)
    # Get the index of most similarity
    n = cor.argmax()
    return signal[n:n+SAMPLE_RATE]


def get_signal_frames(signal, n=None):
    """
    Return a list holding 20ms (default) frames of the signal.

    :param n: Number of frames
    :type n: int
    """
    if n is None:
        n = ms2sample(20)
    n = max(1, n)  # limit the minimum chunk size to 1
    return list(chunks(signal, n, overlap=n//2))


def chunks(lst, n, overlap=0):
    """
    Yield successive n-sized chunks from lst. The chunks do not overlap
    by default, the overlap arg specifies how many elements should overlap.

    This content was inspired by the STACK OVERFLOW network.
    Original question:
     - https://stackoverflow.com/questions/312443
    Author of the question:
     - https://stackoverflow.com/users/112415/jespern
    Author of the relevant answer:
     - https://stackoverflow.com/users/14343/ned-batchelder
    """
    for i in range(0, len(lst), n - overlap):
        yield lst[i:i+n]


def ms2sample(ms, rate=SAMPLE_RATE):
    """Convert the millisecond to sample value. Default is 16,000."""
    return SAMPLE_RATE//1000 * ms


def clip_centre(signal, threshold=0.7):
    """
    Return the clipped signal. Threshold value is in percentages.

    All values above the threshold are set to 1.
    All values belove the negative threshold are set to -1.
    Other values are set to 0.
    """
    pos_max = np.max(signal) * threshold
    neg_max = np.min(signal) * threshold
    def clip(sample):
        if sample > pos_max:
            return 1
        elif sample < neg_max:
            return -1
        return 0

    return np.fromiter((map(clip, signal)), dtype=np.int16)


def auto_correlate(signal):
    """Return the relevant part of the autocorellated signal."""
    cor = np.correlate(signal, signal, 'full')
    return cor[cor.size//2:]


def save_figure(fig, name):
    fig.savefig(OUTPUT_PATH + f'{name}.png')
    fig.savefig(OUTPUT_PATH + f'{name}-transparent.png', transparent=True)
    fig.savefig(OUTPUT_PATH + f'{name}.pdf')
