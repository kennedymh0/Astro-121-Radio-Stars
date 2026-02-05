import numpy as np
import ugradio
import ugradio.dft as dft
from scipy import signal

def compute_power_spectrum(data, sample_rate, method='fft', freq_oversampling=1):
    '''
    power spectrum from time series 
    
    parameters: data=array, sample_rate = sampling rate in Hz, method = dft or fft, 
                freq_oversampling = for dft only (oversample frequency domain by this factor)
    returns: freqs = frequency bins in Hz 
             power = power spectrum
             
    '''
    N = len(data)
    
    if method == 'fft':
        spectrum = np.fft.fft(data)
        freqs = np.fft.fftfreq(N, d=1/sample_rate)
        
        spectrum = np.fft.fftshift(spectrum)
        freqs = np.fft.fftshift(freqs)
        
    elif method == 'dft':
        times = np.arange(-N/2, N/2) / sample_rate
        N_freq = N * freq_oversampling
        freqs = np.linspace(-sample_rate/2, sample_rate/2 * (1 - 2/N_freq), N_freq)
        _, spectrum = dft.dft(data, t-times, f=freqs, vsamp=sample_rate)
        
    else: 
        raise ValueError("choose either fft or dft")
        
    power = np.abs(np.sqrt(spectrum))
    
    return freqs, power

def compute_voltage_spectra(data, sample_rate): 
    N = len(data)
    spectra = np.fft.fft(data)
    freqs = np.fft.fftfreq(N, d=1/sample_rate)    
    
    spectrum = np.sqrt(np.fft.fftshift(spectra))
    freqs = np.fft.fftshift(freqs)
    
    return freqs, spectrum 


def compute_acf(data, max_lag=None):
    '''
    compute autocorrelation function
    note: max_lag = max lag to compute
    returns: lags = lag indices and acf = autocorrelation normalized values
    '''
    N = len(data)
    if max_lag is None: 
        max_lag = N - 1
        
    data_normalized = data - np.mean(data)
    
    acf_full = signal.correlate(data_normalized, data_normalized, mode='full')
    
    acf_full = acf_full / acf_full[N-1]
    
    center = N-1 
    lags = np.arange(-max_lag, max_lag +1)
    acf = acf_full[center - max_lag : center + max_lag + 1]
    
    return lags, acf

def fourier_filter(data, sample_rate, freq_range_to_zero): 
    
    '''
    removes frequency range by zeroing in Fourier domain
    note: freq_range_to_zero = freq range to remove in Hz
    returns: filtered time series 
    '''
    
    spectrum = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(data), d=1/sample_rate)
    
    #filter mask
    f_low, f_high = freq_range_to_zero
    mask = (np.abs(freqs) < f_low) | (np.abs(freqs)>f_high)
    
    spectrum_filtered = spectrum * mask
    
    return filtered

def analyze_noise_stats(data):
    '''
    analyzes statistical properties of noise data
    '''
    stats = {'mean': np.mean(data), 
             'std': np.std(data),
             'variance': np.var(data),
             'min': np.min(data),
             'max': np.max(data),
             'rms': np.sqrt(np.mean(data**2))}
    return stats

def fit_gaussian(data, bins=50):
    '''
    gaussian to data histograms
    returns: hist = histogram counts, bin_centers = bin centers, gaussian fits
    '''
    hist, bin_edges = np.histogram(data, bins=bins, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    mean = np.mean(data)
    std = np.std(data)
    gaussian_fit = (1/ (std * np.sqrt(2*np.pi))) * np.exp(-0.5 * ((bin_centers - mean) / std)**2)
    
    return hist, bin_centers, gaussian_fit

def compute_snr_v_averaging(data_blocks):
    '''
    computes SNR improvement w/ averaging
    '''
    nblocks = data_blocks.shape[0]
    sample_rate = 2.4e6
    
    all_spectra = []
    for block in data_blocks:
        freqs, power = compute_power_spectrum(block, sample_rate)
        all_spectra.append(power)
        
    all_spectra = np.array(all_spectra)
    
    n_avg_list = [1, 2, 4, 8, 16]
    snr_values = []
    
    for n_avg in n_avg_list: 
        if n_avg > nblocks:
            break
            
        avg_spectrum = np.mean(all_spectra[:n_avg], axis=0)
        
        #SNR estimation (signal power/ noise std)
        signal_power = np.max(avg_spectrum)
        noise_std = np.std(avg_spectrum)
        snr = signal_power/noise_std
        snr_values.append(snr)
        
    results = {'navg': n_avg_list[:len(snr_values)],
               'snr': snr_values,
               'freqs': freqs,
               'averaged_spectra': [np.mean(all_spectra[:n], axis=0)
                                    for n in n_avg_list[:len(snr_values)]]
    }

    return results


def find_fwhm(x, y):
    """
 full width at half maximum
    """
    peak_idx = np.argmax(y)
    peak_val = y[peak_idx]
    half_max = peak_val / 2
    
    # points closest to half maximum
    left_idx = np.where(y[:peak_idx] <= half_max)[0]
    right_idx = np.where(y[peak_idx:] <= half_max)[0]
    
    if len(left_idx) > 0 and len(right_idx) > 0:
        left_x = x[left_idx[-1]]
        right_x = x[peak_idx + right_idx[0]]
        fwhm = right_x - left_x
    else:
        fwhm = np.nan
    
    return fwhm
                                    
                                    
                               