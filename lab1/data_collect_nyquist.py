
"""
data for Nyquist sampling 
"""

import os
from datetime import datetime
import numpy as np
import sys
sys.path.insert(0, '../src')

from src.acquiring_data import capture_sine_wave, save_data

## converts frequencies to scientific notation form to reduce file name clutter##
def sci_filename(x, sig=3):
    s = f"{x:.{sig}e}"
    return (
    s.replace('.', 'p')
.replace('+', '')
.replace('-', 'm'))    

def main():
    sample_rates = [1.0e6, 1.5e6, 2.0e6, 2.5e6, 3.0e6] #can also change this 
    signal_freq = 3e6  # 500 kHz; change here for different data 
    nsamples = 2048 #this too maybe
    
    print("="*60)
    print("NYQUIST SAMPLING DATA COLLECTION")
    print("="*60)
    print(f"Signal frequency: {signal_freq/1e3} kHz")
    print("\nSignal generator is set to:")
    print(f"  - Frequency: {signal_freq/1e3} kHz")
    print(f"  - Amplitude: 10 mVpp")
    print("\nPress Enter when ready...")
    input()
    
    ## creates a unique timestamped folder for this block of measurements in which files will be saved to##
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"test_{ts}"
    cwd = os.getcwd()
    path = os.path.join(cwd, folder_name)
    os.makedirs(os.path.join(cwd, folder_name), exist_ok=True)
    
    for sr in sample_rates:
        print(f"\n--- Sample rate: {sr/1e6} MHz ---")
        
        # Capture with filter
        data, metadata = capture_sine_wave(
            signal_freq=signal_freq,
            sample_rate=sr,
            nsamples=nsamples,
            bypass_filter=False
        )
        
        # another unique timestamp so as to have unique file names for each measurement
        sci_sig = sci_filename(signal_freq)
        sci_sr = sci_filename(sr)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  
        
        filename = f"filtered_f{sci_sig}_sr{sci_sr}_{timestamp}.npz"
        save_data(data, metadata, filename, path)
        
        # Capture without filter
        data, metadata = capture_sine_wave(
            signal_freq=signal_freq,
            sample_rate=sr,
            nsamples=nsamples,
            bypass_filter=True
        )
        

        
        filename = f"bypassed_f{sci_sig}_sr{sci_sr}_{timestamp}.npz"
        save_data(data, metadata, filename, path)
    
    print("\n" + "="*60)
    print("Data collection complete")
    print("="*60)
    
    

if __name__ == '__main__':
    main()