'''
i/q mixer data collection
'''

import os
import numpy as np
import sys
sys.path.insert(0, '../src')
from datetime import datetime

from src.acquiring_data import capture_iq_mixer, save_data
def sci_filename(x, sig=3):
    s = f"{x:.{sig}e}"
    return (
    s.replace('.', 'p')
.replace('+', '')
.replace('-', 'm'))      
def main():
    sample_rate = 2.4e6 
    nsamples = 16384
    lo_freq = 10e6

    print("="*60)
    print("MIXER COLLECTION")
    print("="*60)
    print("Press Enter when ready")
    input()
## creates a unique timestamped folder for this block of measurements in which files will be saved to##
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"test_ng__{ts}"
    cwd = os.getcwd()
    path = os.path.join(cwd, folder_name)
    os.makedirs(os.path.join(cwd, folder_name), exist_ok=True)
    #collecting mixer data
    data, metadata = capture_iq_mixer(
        sample_rate=sample_rate, 
        nsamples=nsamples, 
        nblocks=nblocks, 
    )
# another unique timestamp so as to have unique file names for each measurement
    sci_sr = sci_filename(sample_rate)
    sci_samples = sci_filename(nsamples)
    sci_lo = sci_filename(lo_freq)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  
        
    filename = f"mixer_sr{sci_sr}_lo_freq{sci_lo}_samples{sci_samples}_{timestamp}.npz"
    save_data(data, metadata, filename, path)

    print("\n collection done :>")

if __name__ == '__main__':
    main()

    