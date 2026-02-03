import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, stats
import ugradio.dft as dft

from src import plotting_stuff, analysis, acquiring_data

plotting_stuff.setup_plot_style()

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
      

fig, axes = plt.subplots(len(nyquist_data), 1, figsize=(12, 10), sharex=True)

for ax, (sr, ds) in zip(axes, nyquist_data.items()):
    # Compute power spectrum
    haha = ds['sample_rate']
    freqs, power = analysis.compute_power_spectrum(
        ds['data'], haha, method='fft'
    )
    
    signal_freq = ds['signal_freq']
    nyquist = haha / 2
    
    # Plot
    ax.semilogy(freqs/1e3, power, linewidth=0.8)
    ax.axvline(signal_freq/1e3, color='r', linestyle='--', 
               linewidth=2, label=f'True signal: {signal_freq/1e3:.0f} kHz')
    ax.axvline(nyquist/1e3, color='g', linestyle=':', 
               linewidth=2, alpha=0.7, label=f'Nyquist: {nyquist/1e3:.0f} kHz')
    ax.axvline(-nyquist/1e3, color='g', linestyle=':', 
               linewidth=2, alpha=0.7)
    
    # Determine if aliasing occurs
    if signal_freq < nyquist:
        status = "No aliasing (below Nyquist)"
    else:
        aliased_freq = haha - signal_freq
        ax.axvline(aliased_freq/1e3, color='orange', linestyle='-.', 
                   linewidth=2, label=f'Aliased: {aliased_freq/1e3:.0f} kHz')
        status = f"Aliasing! Appears at {aliased_freq/1e3:.0f} kHz"
    
    ax.set_ylabel('Power (arb)')
    ax.set_title(f'$f_s$ = {haha/1e6:.1f} MHz — {status}')
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim([-haha/2/1e3*1.1, haha/2/1e3*1.1])

axes[-1].set_xlabel('Frequency (kHz)')
plt.tight_layout()
plt.savefig('../data/test.png', dpi=300, bbox_inches='tight')
plt.show()

