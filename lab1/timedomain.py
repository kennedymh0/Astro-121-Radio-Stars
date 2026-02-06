import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, stats
import ugradio.dft as dft

from src import plotting_stuff, analysis, acquiring_data

plotting_stuff.setup_plot_style()

nyquist_files = [
    '/home/radiopi/Astro-121-Radio-Stars/lab1/test_md_radio_20260206_014212/mixer_sr2p400e06_lo_freq1p000e08_samples1p638e04_20260206_014215.npz',
'/home/radiopi/Astro-121-Radio-Stars/lab1/test_md_radio_20260206_014212/mixer_sr2p400e06_lo_freq1p000e08_samples1p638e04_20260206_014241.npz'
]

nyquist_data = {}
for file in nyquist_files:
    loaded = np.load(file)
    sr = loaded['sample_rate']
    nyquist_data[file] = {
        'data': loaded['data'],
        'sample_rate': sr
    }
    


for i in nyquist_data.keys():
    samp_rate = nyquist_data.get(i).get('sample_rate')
    dt = nyquist_data.get(i).get('data')[0]
    print(dt)
    t = np.arange(len(dt)) / samp_rate
    plt.figure(figsize=(10,4))
    plt.plot(t[:100]*1e6, dt[:100])
    plt.xlabel("Time (microseconds)")
    plt.ylabel("Amplitude")
    plt.title("Time-Domain RF Signal (~1MHz)")
    plt.grid(True)
    plt.show()