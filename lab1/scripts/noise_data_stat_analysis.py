
"""
noise data for statistical analysis
"""

import numpy as np
import sys
sys.path.insert(0, '../src')

from radiolab.acquiring_data import capture_noise, save_data

def main():
    sample_rate = 2.4e6 #change
    nsamples = 16384 #change
    nblocks = 16 #change
    
    print("="*60)
    print("NOISE DATA COLLECTION")
    print("="*60)
    print("\nConnect noise generator to SDR input")
    print("Press Enter when ready...")
    input()
    
    # Collect multiple blocks for averaging analysis
    data, metadata = capture_noise(
        sample_rate=sample_rate,
        nsamples=nsamples,
        nblocks=nblocks
    )
    
    filename = f"../data/noise/noise_{nblocks}blocks_{nsamples}samples.npz"
    save_data(data, metadata, filename)
    
    print("\n collection complete")

if __name__ == '__main__':
    main()