import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, stats
import ugradio.dft as dft

from src import plotting_stuff, analysis, acquiring_data

plotting_stuff.setup_plot_style()

nyquist_files = [
    '../data/nyquist/bypassed_f1000000_sr2000000.npz'
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