
"""
data for Nyquist sampling 
"""

import numpy as np
import sys
sys.path.insert(0, '../src')

from src.acquiring_data import capture_sine_wave, save_data

def main():
    sample_rates = [1.0e6, 1.5e6, 2.0e6, 2.5e6, 3.0e6] #can also change this 
    signal_freq = 75e4  # 100 kHz; change here for different data 
    nsamples = 16384 #this too maybe
    
    print("="*60)
    print("NYQUIST SAMPLING DATA COLLECTION")
    print("="*60)
    print(f"Signal frequency: {signal_freq/1e3} kHz")
    print("\nSignal generator is set to:")
    print(f"  - Frequency: {signal_freq/1e3} kHz")
    print(f"  - Amplitude: 10 mVpp")
    print("\nPress Enter when ready...")
    input()
    
    for sr in sample_rates:
        print(f"\n--- Sample rate: {sr/1e6} MHz ---")
        
        # Capture with filter
        data, metadata = capture_sine_wave(
            signal_freq=signal_freq,
            sample_rate=sr,
            nsamples=nsamples,
            bypass_filter=False
        )
        
        filename = f"../data/nyquist/filtered_f{signal_freq:.0f}_sr{sr:.0f}.npz"
        save_data(data, metadata, filename)
        
        # Capture without filter
        data, metadata = capture_sine_wave(
            signal_freq=signal_freq,
            sample_rate=sr,
            nsamples=nsamples,
            bypass_filter=True
        )
        
        filename = f"../data/nyquist/bypassed_f{signal_freq:.0f}_sr{sr:.0f}.npz"
        save_data(data, metadata, filename)
    
    print("\n" + "="*60)
    print("Data collection complete")
    print("="*60)

if __name__ == '__main__':
    main()