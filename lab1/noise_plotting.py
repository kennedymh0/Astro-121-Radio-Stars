noise_file = np.load('../data/noise/noise_16blocks_16384samples.npz')
noise_data = noise_file['data']  # Shape: (16, 16384)

print(f"Noise data shape: {noise_data.shape}")

# Analyze one block
block0 = noise_data[0]
stats = analysis.analyze_noise_statistics(block0)

print("\nStatistical properties (single block):")
for key, val in stats.items():
    print(f"  {key:10s}: {val:8.3f}")

# Histogram vs Gaussian
hist, bin_centers, gaussian_fit = analysis.fit_gaussian(block0, bins=50)

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(bin_centers, hist, width=bin_centers[1]-bin_centers[0], 
       alpha=0.7, label='Measured histogram')
ax.plot(bin_centers, gaussian_fit, 'r-', linewidth=2, 
       label=f'Gaussian fit (μ={stats["mean"]:.2f}, σ={stats["std"]:.2f})')
ax.set_xlabel('Amplitude')
ax.set_ylabel('Probability Density')
ax.set_title('Noise Distribution vs Gaussian')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../plots/noise_distribution.png', dpi=300, bbox_inches='tight')
plt.show()