import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, stats
import ugradio.dft as dft
from src import plotting_stuff, analysis, acquiring_data

plotting_stuff.setup_plot_style()

# Load data
file = "/home/radiopi/Astro-121-Radio-Stars/lab1/test_ng__20260204_232835/noise_sr3p000e06_1p600e01_samples1p638e04_20260204_232836.npz"

noise_file = np.load(file)
noise_data = noise_file['data']  # Shape: (16, 16384)

print(f"Noise data shape: {noise_data.shape}")

# Analyze one block
block0 = noise_data[0]
stats = analysis.analyze_noise_stats(block0)
print(stats)

print(f"here are the unique elements in the first noise data block: {np.unique(block0)}")
remove_one = block0[(block0 != 1) & (block0 != -1)]

mean = stats['mean']
std = stats['std']
valid_range = 1

mask = np.abs(block0 - mean) <= valid_range*std
data_filtered = block0[mask]


# Histogram vs Gaussian
hist, bin_centers, gaussian_fit = analysis.fit_gaussian(remove_one, bins=300)

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(bin_centers, hist, width=bin_centers[1]-bin_centers[0], 
       alpha=0.7, label='Measured histogram')
ax.plot(bin_centers, gaussian_fit, 'r-', linewidth=2, 
       label=f'Gaussian fit (μ={stats["mean"]:.2f}, σ={stats["std"]:.2f})')
ax.set_xlabel('Amplitude')
ax.set_ylabel('Probability Density')
ax.set_title('Noise Distribution vs Gaussian')
ax.set_xlim([mean - 3*std, mean + 3*std])
ax.set_ylim([0, 1])

for n_sigma in [1, 2, 3]:
    ax.axvline(mean + n_sigma*std, color='gray', linestyle='--', linewidth=1, alpha = 0.5)
    ax.axvline(mean - n_sigma*std, color='gray', linestyle='--', linewidth=1, alpha =0.5)
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../noise_distribution.png', dpi=300, bbox_inches='tight')
plt.show()