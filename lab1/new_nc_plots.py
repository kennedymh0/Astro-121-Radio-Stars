import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, stats
import ugradio.dft as dft
from src import plotting_stuff, analysis, acquiring_data

# Setup plotting
plotting_stuff.setup_plot_style()

# Load data
nyquist_files = [
    '../data/nyquist/filtered_f100000_sr1000000.npz',
    '../data/nyquist/filtered_f100000_sr2000000.npz',
    '../data/nyquist/filtered_f100000_sr2400000.npz',
    '../data/nyquist/filtered_f100000_sr3200000.npz',
]

nyquist_data = {}
for file in nyquist_files:
    loaded = np.load(file)
    sr = loaded['sample_rate']
    nyquist_data[file] = {
        'data': loaded['data'],
        'signal_freq': loaded['signal_freq'],
        'sample_rate': sr
    }

# ============================================================================
# COMBINED VISUALIZATION: Time Series + Spectra + Nyquist Zones
# ============================================================================

n_datasets = len(nyquist_data)
fig = plt.figure(figsize=(18, 4*n_datasets))
gs = fig.add_gridspec(n_datasets, 3, hspace=0.35, wspace=0.35)

for row_idx, (file, ds) in enumerate(nyquist_data.items()):
    # Extract data
    data = ds['data']
    signal_freq = ds['signal_freq']
    sr = ds['sample_rate']
    nyquist = sr / 2
    
    # Compute power spectrum
    freqs, power = analysis.compute_power_spectrum(data, sr, method='fft')
    measured_freq = abs(freqs[np.argmax(power)])
    
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
    # COLUMN 0: TIME SERIES (Sine Wave)
    # =================================================================
    ax_time = fig.add_subplot(gs[row_idx, 0])
    
    # Time array
    t = np.arange(len(data)) / sr * 1e6  # microseconds
    
    # Plot first portion to see waveform clearly
    n_display = min(1000, len(data))
    ax_time.plot(t[:n_display], data[:n_display], 
                linewidth=1.2, color='darkblue', alpha=0.8)
    
    # Formatting
    ax_time.set_ylabel('Amplitude (ADC units)', fontsize=10)
    ax_time.grid(True, alpha=0.3)
    ax_time.set_xlim([0, t[n_display-1]])
    
    # Title with sampling rate
    ax_time.set_title(f'Sampled Waveform\n$f_s$ = {sr/1e6:.1f} MHz', 
                     fontsize=11, fontweight='bold')
    
    # Info box
    info_text = (f'True freq: {signal_freq/1e3:.0f} kHz\n'
                f'Nyquist: {nyquist/1e3:.0f} kHz\n'
                f'Measured: {measured_freq/1e3:.0f} kHz')
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
    
    # Plot spectrum
    ax_spec.semilogy(freqs/1e3, power, linewidth=1, color='navy', alpha=0.8)
    
    # Shade Nyquist zones
    # 1st Nyquist zone: [-fs/2, fs/2] (GREEN - safe zone)
    ax_spec.axvspan(-nyquist/1e3, nyquist/1e3, alpha=0.12, color='green',
                   label='1st Nyquist zone', zorder=0)
    
    # 2nd Nyquist zones: [fs/2, fs] and [-fs, -fs/2] (YELLOW - will alias)
    ax_spec.axvspan(nyquist/1e3, sr/1e3, alpha=0.12, color='yellow',
                   label='2nd Nyquist zone', zorder=0)
    ax_spec.axvspan(-sr/1e3, -nyquist/1e3, alpha=0.12, color='yellow', zorder=0)
    
    # Draw Nyquist boundaries
    ax_spec.axvline(nyquist/1e3, color='green', linestyle=':', 
                   linewidth=2, alpha=0.7, label=f'Nyquist: ±{nyquist/1e3:.0f} kHz')
    ax_spec.axvline(-nyquist/1e3, color='green', linestyle=':', 
                   linewidth=2, alpha=0.7)
    
    # Draw sampling rate boundaries (edges of observable range)
    ax_spec.axvline(sr/1e3, color='orange', linestyle=':', 
                   linewidth=1.5, alpha=0.4)
    ax_spec.axvline(-sr/1e3, color='orange', linestyle=':', 
                   linewidth=1.5, alpha=0.4)
    
    # Mark TRUE signal frequency
    ax_spec.axvline(signal_freq/1e3, color='red', linestyle='--', 
                   linewidth=2.5, alpha=0.85,
                   label=f'True signal: {signal_freq/1e3:.0f} kHz')
    
    # If aliasing, mark the ALIASED frequency
    if is_aliasing:
        ax_spec.axvline(aliased_freq/1e3, color='darkorange', linestyle='-.', 
                       linewidth=2.5, alpha=0.85,
                       label=f'Appears at: {aliased_freq/1e3:.0f} kHz')
    
    # Formatting
    ax_spec.set_ylabel('Power (arb)', fontsize=10)
    ax_spec.set_title(f'Power Spectrum with Nyquist Zones\n{status}', 
                     fontsize=11, fontweight='bold', color=status_color)
    ax_spec.legend(loc='upper right', fontsize=8, framealpha=0.9)
    ax_spec.grid(True, alpha=0.3)
    ax_spec.set_xlim([-sr/2/1e3*1.15, sr/2/1e3*1.15])
    
    # Set reasonable y-limits
    power_positive = power[power > 0]
    if len(power_positive) > 0:
        ax_spec.set_ylim([power_positive.min() * 0.5, power.max() * 5])
    
    if row_idx == n_datasets - 1:
        ax_spec.set_xlabel('Frequency (kHz)', fontsize=10)
    
    # =================================================================
    # COLUMN 2: ZOOMED SPECTRUM (around peak)
    # =================================================================
    ax_zoom = fig.add_subplot(gs[row_idx, 2])
    
    # Find peak and create zoom window
    peak_idx = np.argmax(power)
    peak_freq = freqs[peak_idx]
    zoom_range = max(100e3, sr/20)  # Adaptive zoom range
    
    mask = (freqs > peak_freq - zoom_range) & (freqs < peak_freq + zoom_range)
    
    # Plot zoomed spectrum
    ax_zoom.plot(freqs[mask]/1e3, power[mask], 
                linewidth=2, color='darkblue', marker='o', 
                markersize=2, alpha=0.7)
    
    # Mark the measured peak
    ax_zoom.axvline(peak_freq/1e3, color='blue', linestyle='-', 
                   linewidth=2, alpha=0.6, 
                   label=f'Measured: {abs(peak_freq)/1e3:.1f} kHz')
    
    # Mark expected frequency
    if is_aliasing:
        expected = aliased_freq
        ax_zoom.axvline(expected/1e3, color='darkorange', linestyle='--', 
                       linewidth=2, alpha=0.7, 
                       label=f'Expected (aliased): {expected/1e3:.1f} kHz')
        # Show original frequency as reference
        ax_zoom.text(0.5, 0.95, 
                    f'Original: {signal_freq/1e3:.0f} kHz\n(above Nyquist)',
                    transform=ax_zoom.transAxes, ha='center', va='top',
                    fontsize=8, color='red',
                    bbox=dict(boxstyle='round', facecolor='pink', alpha=0.7))
    else:
        expected = signal_freq
        ax_zoom.axvline(expected/1e3, color='red', linestyle='--', 
                       linewidth=2, alpha=0.7, 
                       label=f'Expected: {expected/1e3:.1f} kHz')
    
    # Formatting
    ax_zoom.set_ylabel('Power (arb)', fontsize=10)
    ax_zoom.set_title(f'Zoomed Spectrum\n(±{zoom_range/1e3:.0f} kHz around peak)', 
                     fontsize=11, fontweight='bold')
    ax_zoom.legend(loc='upper right', fontsize=8)
    ax_zoom.grid(True, alpha=0.3)
    
    # Calculate and display error
    error = abs(measured_freq - expected) / expected * 100
    ax_zoom.text(0.02, 0.05, f'Error: {error:.2f}%',
                transform=ax_zoom.transAxes, fontsize=9,
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    
    if row_idx == n_datasets - 1:
        ax_zoom.set_xlabel('Frequency (kHz)', fontsize=10)

# Overall title
fig.suptitle('Nyquist Sampling Theorem: Complete Demonstration\n'
             f'Signal: {signal_freq/1e3:.0f} kHz sine wave at various sampling rates', 
             fontsize=15, fontweight='bold', y=0.998)

plt.savefig('../data/nyquist_complete_combined.png', dpi=300, bbox_inches='tight')
plt.show()



