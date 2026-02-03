
import numpy as np
import matplotlib.pyplot as plt


def setup_plot_style():
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['font.size'] = 11
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 13
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 300


def plot_time_series(t, data, title='Time Series', xlabel='Time (s)', 
                    ylabel='Amplitude', xlim=None, save_path=None):
    """
    plot time series data
    """
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(t, data, linewidth=0.8)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    
    if xlim is not None:
        ax.set_xlim(xlim)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_spectrum(freqs, power, title='Power Spectrum', 
                 log_scale=True, signal_freq=None, nyquist_freq=None,
                 xlim=None, save_path=None):
  
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if log_scale:
        ax.semilogy(freqs/1e3, power, linewidth=0.8)
    else:
        ax.plot(freqs/1e3, power, linewidth=0.8)
    
    if signal_freq is not None:
        ax.axvline(signal_freq/1e3, color='viridis', linestyle='--', 
                  linewidth=2, label=f'Signal: {signal_freq/1e3:.1f} kHz')
    
    if nyquist_freq is not None:
        ax.axvline(nyquist_freq/1e3, color='plasma', linestyle=':', 
                  linewidth=2, label=f'Nyquist: {nyquist_freq/1e3:.1f} kHz')
        ax.axvline(-nyquist_freq/1e3, color='plasma', linestyle=':', 
                  linewidth=2)
    
    ax.set_xlabel('Frequency (kHz)')
    ax.set_ylabel('Power (arb)')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    if xlim is not None:
        ax.set_xlim([x/1e3 for x in xlim])
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()