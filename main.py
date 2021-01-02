#!/usr/bin/env python

# Author: Marek Filip <wecros|xfilip46>
# Date: 2020/12/27

import sys
import wave

import matplotlib.pyplot as plt
import numpy as np

from sklearn.preprocessing import minmax_scale
from lib import open_wave, centralize_signal, normalize_signal

import ex3
import ex4


def main():
    save = False
    if len(sys.argv) > 1 and sys.argv[1] == '--save':
        save = True

    ex3.main(save)
    ex4.main(save)

    if save:
        print('All graphs saved to the "output" folder')


if __name__ == '__main__':
    main()
