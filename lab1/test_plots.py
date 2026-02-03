import numpy as np
import sys
sys.path.insert(0, '../src')

from src import plotting_stuff

plotting_stuff.setup_plot_style()

nyquist_files = [
    '../data/nyquist/bypassed_f100000_sr1000000.npz',
    '../data/nyquist/bypassed_f100000_sr2000000.npz',
    '../data/nyquist/bypassed_f100000_sr2400000.npz',
    '../data/nyquist/bypassed_f100000_sr3200000.npz'
]

nyquist_data = {}
for blah in nyquist_data:
    loaded = np.load(blah)
    sr = ;paded['sample_rate']
    nyquist_data[sr] = {
        'data': loaded['data'],
        'signal_freq': loaded['signal_freq'],
        'sample_rate': sr
    }
    
fig, axes
