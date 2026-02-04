import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, stats
import ugradio.dft as dft

from src import plotting_stuff, analysis, acquiring_data

plotting_stuff.setup_plot_style()

key = "20260203_140125" # change to relevant test folder key
cwd = os.getcwd()
test_folder = f"test_{key}"
path = os.path.join(cwd, test_folder)
nyquist_files = os.listdir(path)

nyquist_data = {}
for file in nyquist_files:
    loaded = np.load(os.path.join(path, file))
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
        status = f"Aliasing appears at {aliased_freq/1e3:.0f} kHz"
    
    ax.set_ylabel('Power (arb)')
    ax.set_title(f'$f_s$ = {haha/1e6:.1f} MHz — {status}')
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim([-haha/2/1e3*1.1, haha/2/1e3*1.1])

axes[-1].set_xlabel('Frequency (kHz)')
plt.tight_layout()
plt.savefig('../data/test.png', dpi=300, bbox_inches='tight')
plt.show()


ncol = 3
nrow = (len(nyquist_data) + 1) // 2
fig, axes = plt.subplots(nrow, ncol, figsize=(10, 4*nrow), sharex=True)
    
    
for i, (k, v) in enumerate(nyquist_data.items()):
    z = i%3 # modulo i to retrieve relevant column index
    j = (i)//3
    
    s_r = v['sample_rate']
    signal_freq = v['signal_freq']
    data = v['data'][0]
    nsamples = len(data)
    t = np.arange(nsamples) / signal_freq
    axes[j][z].plot(t[:100]*1e6, data[:100])
    axes[j][z].set_title(f"{s_r:.2} MHz")
    axes[j][z].set_xlabel(r"Time $\mu$")
    axes[j][z].set_ylabel("Amplitude")
    axes[j][z].grid(True)
    
plt.tight_layout()
plt.show()


