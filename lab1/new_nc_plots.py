import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, stats
import ugradio.dft as dft
from src import plotting_stuff, analysis, acquiring_data

# Setup plotting
plotting_stuff.setup_plot_style()

# Load data
path = "/home/radiopi/Astro-121-Radio-Stars/lab1/test_20260204_155612"
nyquist_files = os.listdir(path)


# Load and verify data structure
nyquist_data = {}
for file in nyquist_files:
    loaded = np.load(os.path.join(path, file))

    sr = loaded['sample_rate']
    data = loaded['data']
    
    # SAFETY: Ensure data is 1D
    print(f"\nLoading {file}")
    print(f"  Original data shape: {data.shape}")
    
    if data.ndim > 1:
        print(f"  WARNING: Data is {data.ndim}D, converting to 1D")
        data = data.squeeze()  # Remove singleton dimensions
        
    if data.ndim > 1:
        print(f"  Still {data.ndim}D after squeeze, taking first row")
        data = data[0]
    
    print(f"  Final data shape: {data.shape} ✓")
    
    nyquist_data[file] = {
        'data': data,
        'signal_freq': loaded['signal_freq'],
        'sample_rate': sr
    }

# ============================================================================
# COMBINED VISUALIZATION: Time Series + Spectra + Nyquist Zones
# ============================================================================

n_datasets = len(nyquist_data)
fig = plt.figure(figsize=(18, 4*n_datasets))
gs = fig.add_gridspec(n_datasets, 2, hspace=0.35, wspace=0.35)

for row_idx, (file, ds) in enumerate(nyquist_data.items()):
    # Extract data
    data = ds['data']
    signal_freq = ds['signal_freq']
    sr = ds['sample_rate']
    nyquist = sr / 2
    
    # Ensure 1D (redundant but safe)
    if data.ndim > 1:
        data = data.flatten()
    
    print(f"\nProcessing row {row_idx}:")
    print(f"  Data length: {len(data)}")
    
    # Compute power spectrum
    try:
        freqs, power = analysis.compute_power_spectrum(data, sr, method='fft')
        print(f"  Freqs length: {len(freqs)}")
        print(f"  Power length: {len(power)}")
        
        # Verify match
        if len(freqs) != len(power):
            raise ValueError(f"Length mismatch: freqs={len(freqs)}, power={len(power)}")
        
        # Find peak safely
        peak_idx = np.argmax(power)
        measured_freq = abs(freqs[peak_idx])
        print(f"  Peak index: {peak_idx}, Measured freq: {measured_freq/1e3:.4f} kHz ✓")
        
    except Exception as e:
        print(f"  ERROR: {e}")
        raise
    # compute voltage spectra
    try:
        freqs, voltage = analysis.compute_voltage_spectra(data, sr)
        print(f"  Freqs length: {len(freqs)}")
        print(f"  Voltage length: {len(voltage)}")
        
        # Verify match
        if len(freqs) != len(voltage):
            raise ValueError(f"Length mismatch: freqs={len(freqs)}, power={len(voltage)}")
        
        # Find peak safely
        peak_idx = np.argmax(voltage)
        measured_freq = abs(freqs[peak_idx])
        print(f"  Peak index: {peak_idx}, Measured freq: {measured_freq/1e3:.4f} kHz ✓")
        
    except Exception as e:
        print(f"  ERROR: {e}")
        raise
    # Determine if aliasing occurs
    is_aliasing = signal_freq > nyquist
    if is_aliasing:
        aliased_freq = sr - signal_freq
        status = f"ALIASING: {signal_freq/1e3:.0f}→{aliased_freq/1e3:.0f} kHz"
        status_color = 'red'
    else:
        status = "No Aliasing (fs > 2f)"
        status_color = 'green'
    
    # =================================================================
    # COLUMN 0: TIME SERIES
    # =================================================================
    ax_time = fig.add_subplot(gs[row_idx, 0])
    
    t = np.arange(len(data)) / sr * 1e3  # microseconds
    n_display = min(25, len(data))
    ax_time.plot(t[:n_display], data[:n_display], 
                linewidth=1.2, color='darkblue', alpha=0.8)
    
    ax_time.set_ylabel('Amplitude', fontsize=10)
    ax_time.grid(True, alpha=0.3)
    ax_time.set_xlim([0, t[n_display-1]])
    ax_time.set_title(f'Sampled Waveform\n$f_s$ = {sr/1e6:.1f} MHz', 
                     fontsize=11, fontweight='bold')
    
    info_text = (f'True freq: {signal_freq/1e3:.0f} kHz\n'
                f'Nyquist: {nyquist/1e3:.0f} kHz\n'
                f'Measured: {measured_freq/1e3:.4f} kHz')
    ax_time.text(0.98, 0.97, info_text,
                transform=ax_time.transAxes,
                fontsize=9, verticalalignment='top',
                horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    if row_idx == n_datasets - 1:
        ax_time.set_xlabel('Time (μs)', fontsize=10)
    
    # =================================================================
    # COLUMN 1: FULL SPECTRUM with Nyquist Zones
    # =================================================================
    ax_spec = fig.add_subplot(gs[row_idx, 1])
    
    ax_spec.semilogy(freqs/1e3, power, linewidth=1, color='navy', alpha=0.8)
    
    # Shade Nyquist zones
    ax_spec.axvspan(-nyquist/1e3, nyquist/1e3, alpha=0.12, color='green',
                   label='1st Nyquist zone', zorder=0)
    ax_spec.axvspan(nyquist/1e3, sr/1e3, alpha=0.12, color='yellow',
                   label='2nd Nyquist zone', zorder=0)
    ax_spec.axvspan(-sr/1e3, -nyquist/1e3, alpha=0.12, color='yellow', zorder=0)
    
    # Draw boundaries
    ax_spec.axvline(nyquist/1e3, color='green', linestyle=':', 
                   linewidth=2, alpha=0.7, label=f'Nyquist: ±{nyquist/1e3:.0f} kHz')
    ax_spec.axvline(-nyquist/1e3, color='green', linestyle=':', 
                   linewidth=2, alpha=0.7)
    
    # Mark frequencies
    ax_spec.axvline(signal_freq/1e3, color='red', linestyle='--', 
                   linewidth=2.5, alpha=0.85,
                   label=f'True signal: {signal_freq/1e3:.0f} kHz')
    
    if is_aliasing:
        ax_spec.axvline(aliased_freq/1e3, color='darkorange', linestyle='-.', 
                       linewidth=2.5, alpha=0.85,
                       label=f'Appears at: {aliased_freq/1e3:.0f} kHz')
    
    ax_spec.set_ylabel('Power (arb)', fontsize=10)
    ax_spec.set_title(f'Power Spectrum with Nyquist Zones\n{status}', 
                     fontsize=11, fontweight='bold', color=status_color)
    ax_spec.legend(loc='upper right', fontsize=8, framealpha=0.9)
    ax_spec.grid(True, alpha=0.3)
    ax_spec.set_xlim([0, sr/2/1e3*1.15])
    
    power_positive = power[power > 0]
    if len(power_positive) > 0:
        ax_spec.set_ylim([power_positive.min() * 0.5, power.max() * 5])
    
    if row_idx == n_datasets - 1:
        ax_spec.set_xlabel('Frequency (kHz)', fontsize=10)

fig.suptitle('Nyquist Sampling \n'
             f'Signal: {signal_freq/1e3:.0f} kHz sine wave at various sampling rates', 
             fontsize=15, fontweight='bold', y=0.998)

plt.savefig('../data/nyquist_complete_combined.png', dpi=300, bbox_inches='tight')
plt.show()