import os
import numpy as np
import ugradio
import ugradio.sdr
from pathlib import Path
from datetime import datetime

fir_coeff = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2047])
fir_coeff2 = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2047])


def capture_sine_wave(signal_freq, sample_rate=2.4e6, nsamples=16384, bypass_filter=False, direct_sampling=True):
    '''
    captures sine wave from function generator with sdr
    
    parameters: signal_freq = signal frequency in Hz
                sample_rate = sampling rate in Hz
                nsamples = number of samples
                bypass_filter = bypassing anti-aliasing fliter using the fir_coeffs array
                direct_sampling = sampling mode
                
    returns: data = time series data
             metadata = capture parameters
             
    '''
    
    if bypass_filter:
        sdr = ugradio.sdr.SDR(device_index=0, direct=direct_sampling, sample_rate=sample_rate, gain=0, fir_coeffs = fir_coeff)
        filter_status = "bypassed"
        
    else: 
        sdr = ugradio.sdr.SDR(device_index=0, direct=direct_sampling, sample_rate=sample_rate, gain=0)
        filter_status = "filter is on"
        
    print(f"Capturing: {signal_freq/1e3:.1f} kHz at {sample_rate/1e6:.2f} MHz")
    print(f"Filter: {filter_status}")
    
    first_capture = sdr.capture_data(nsamples=nsamples, nblocks=1)
    data = sdr.capture_data(nsamples=nsamples, nblocks=1)
    
    sdr.close()
    
    metadata = {'signal_freq': signal_freq, 'sample_rate': sample_rate, 'nsamples': nsamples, 'filter_bypassed': bypass_filter,
                'direct_sampling': direct_sampling, 'timestamp': datetime.now().isoformat()}
    return data, metadata


def capture_ng(sample_rate=2.4e6, nsamples=16384, nblocks=1):
    '''
    capture data from noise generator
    
    parameters: sample_rate = sampling rate in Hz
                nsamples = number of samples
                nblocks = number of blocks to capture
    returns: data = time series data
             metadata = capture parameters
    '''
    direct_sampling = True
    sdr = ugradio.sdr.SDR(device_index=0, direct=direct_sampling, sample_rate=sample_rate, gain=0)
    print(f"Capturing data: {nblocks} blocks of {nsamples} samples")
    first_capture = sdr.capture_data(nsamples=nsamples, nblocks=nblocks)
    data = sdr.capture_data(nsamples=nsamples, nblocks=nblocks)
    sdr.close()
    
    metadata = {'sample_rate': sample_rate, 'nsamples': nsamples, 'nblocks': nblocks,
                'direct_sampling': True,  'timestamp': datetime.now().isoformat()}
    print(np.unique(data[0]))
    return data, metadata


def capture_iq_mixer(sample_rate=2.4e6, nsamples=16384, lo_freq=10e6):
    '''
    capture I/Q data from SDR internal mixer (SSB mode)
    parameters: sample_rate = sampling rate in Hz
                nsamples = number of samples
                lo_freq = local oscillator frequency in Hz
    returns: data = complex I/Q times series 
             metadata = capture parameters
    '''
    sdr = ugradio.sdr.SDR(device_index=0, direct=False, center_freq=lo_freq, sample_rate=sample_rate, gain=0, fir_coeffs=fir_coeff)
    print(f"Capturing I/Q data: LO = {lo_freq/1e6:.2f} MHz")
    first_capture = sdr.capture_data(nsamples=nsamples, nblocks=1)
    data = sdr.capture_data(nsamples=nsamples, nblocks=1)
    sdr.close()
    
    #combining I and Q to make complex array
    if data.ndim == 2:
        complex_data = data[:,0] + 1j * data[:,1]
    else: 
        complex_data = data
    
    metadata = {'sample_rate': sample_rate, 'nsamples': nsamples, 'lo_freq': lo_freq,
                'direct_sampling':False, 'timestamp': datetime.now().isoformat()}
    return data, metadata


def save_data(data, metadata, filename, directory):
    '''
    paramters: data=array, metadata=dictionary, filename=output filename
    '''
    np.savez(os.path.join(directory, filename), data=data, **metadata)
    print(f"Saved: {filename}")
