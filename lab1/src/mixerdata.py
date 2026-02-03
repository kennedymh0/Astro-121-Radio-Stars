'''
i/q mixer data collection
'''

import numpy as np
import sys
sys.path.insert(0, '../src')

from src.acquiring_data import capture_iq_mixer, save_data

def main():
    sample_rate = 2.4e6 
    nsamples = 16384
    lo_freq = 10e6

    print("="*60)
    print("MIXER COLLECTION")
    print("="*60)
    print("Press Enter when ready")
    input()

    #collecting mixer data
    data, metadata = capture_iq_mixer(
        sample_rate=sample_rate, 
        nsamples=nsamples, 
        nblocks=nblocks, 
    )

    filename = f"../data/mixer/mixer_sample_rate_{sample_rate}_lofreq{lo_freq}.npz"
    save_data(data, metadata, filename)

    print("\n collection done :>")

if __name__ == '__main__':
    main()

    