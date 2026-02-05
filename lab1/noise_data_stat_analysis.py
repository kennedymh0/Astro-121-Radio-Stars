
"""
noise data for statistical analysis
"""
import os
import numpy as np
import sys
sys.path.insert(0, '../src')
from datetime import datetime

from src.acquiring_data import capture_ng, save_data
## converts frequencies to scientific notation form to reduce file name clutter##
def sci_filename(x, sig=3):
    s = f"{x:.{sig}e}"
    return (
    s.replace('.', 'p')
.replace('+', '')
.replace('-', 'm'))      

def main():
    sample_rate = 3.5e6 #change
    nsamples = 16384 #change
    nblocks = 16 #change
    
    print("="*60)
    print("NOISE DATA COLLECTION")
    print("="*60)
    print("\nConnect noise generator to SDR input")
    print("Press Enter when ready...")
    input()
    ## creates a unique timestamped folder for this block of measurements in which files will be saved to##
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"test_ng__{ts}"
    cwd = os.getcwd()
    path = os.path.join(cwd, folder_name)
    os.makedirs(os.path.join(cwd, folder_name), exist_ok=True)
    
    # Collect multiple blocks for averaging analysis
    data, metadata = capture_ng(
        sample_rate=sample_rate,
        nsamples=nsamples,
        nblocks=nblocks
    )
    
    # another unique timestamp so as to have unique file names for each measurement
    sci_sr = sci_filename(sample_rate)
    sci_samples = sci_filename(nsamples)
    sci_blocks = sci_filename(nblocks)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  
        
    filename = f"noise_sr{sci_sr}_{sci_blocks}_samples{sci_samples}_{timestamp}.npz"
    save_data(data, metadata, filename, path)
    
    print("\n collection complete")

if __name__ == '__main__':
    main()
