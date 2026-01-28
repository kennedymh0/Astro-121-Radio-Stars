import ugradio 
import ugradio.sdr
import ugradio.dft
import numpy as np
import astropy
import matplotlib.pyplot as plt
radio = ugradio.sdr.SDR(device_index=0)

def compute_spectrum(x, fs):
    x = np.asarray(x)
    x0 = x - np.mean(x)
    
    X = np.fft.fftshift(np.fft.fft(x0))
    f = np.fft.fftshift(np.fft.fftfreq(len(x0), d=1/fs))
    P = np.abs(X)**2
    return f, X, P

def peak_frequency(f, P, fmin=None, fmax=None):
    
    mask = np.ones_like(f, dtype=bool)
    if fmin is not None:
        mask &= (f >= fmin)
    if fmax is not None:
         mask &= (f <= fmax)
            
    idx = np.argmax(P[mask])
    f_peak = f[mask][idx]
    return f_peak
       

fs = 1.0e6
N = 2048
try:
    radio.sample_rate = fs
except Exception:
    radio.sample_rate(fs)
    
try:
    x = radio.read_samples(N)
except Exception:
    try:
        x = radio.read_samples(N)
    except Expection: 
        x = radio.capture_data(N)
        
x = np.asarray(x)
print(x)

t = np.arange(N) / fs

plt.figure()
if np.iscomplexobj(x): 
    plt.plot(t[:100], np.real(x[:100]), label='Re(x)')
    plt.plot(t[:100], np.imag(x[:100]), label='Im(x)')
    plt.legend()
else:
    plt.plot(t[:100],x[:100])
    
plt.xlabel("Time(s)")
plt.ylabel("Voltage")
plt.title("First 100 samples")
plt.show()

fs1 = 2.4e6
N = 2048
try:
    radio.sample_rate = fs1
except Exception:
    radio.sample_rate(fs1)
    
try:
    x1 = radio.read_samples(N)
except Exception:
    try:
        x1 = radio.read_samples(N)
    except Expection: 
        x1 = radio.capture_data(N)
        
x1 = np.asarray(x1)
print(x1)

t1 = np.arange(N) / fs1

plt.figure()
if np.iscomplexobj(x1): 
    plt.plot(t1[:100], np.real(x1[:100]), label='Re(x)')
    plt.plot(t1[:100], np.imag(x1[:100]), label='Im(x)')
    plt.legend()
else:
    plt.plot(t1[:100],x1[:100])
    
plt.xlabel("Time(s)")
plt.ylabel("Voltage")
plt.title("First 100 samples")
plt.show()

fs2 = 3.0e6
N = 2048
try:
    radio.sample_rate = fs2
except Exception:
    radio.sample_rate(fs2)
    
try:
    x2 = radio.read_samples(N)
except Exception:
    try:
        x2 = radio.read_samples(N)
    except Expection: 
        x2 = radio.capture_data(N)
        
x2 = np.asarray(x2)
print(x2)

t2 = np.arange(N) / fs2

plt.figure()
if np.iscomplexobj(x2): 
    plt.plot(t2[:100], np.real(x2[:100]), label='Re(x)')
    plt.plot(t2[:100], np.imag(x2[:100]), label='Im(x)')
    plt.legend()
else:
    plt.plot(t2[:100],x2[:100])
    
plt.xlabel("Time(s)")
plt.ylabel("Voltage")
plt.title("First 100 samples")
plt.show()

fs3 = 3.2e6
N = 2048
try:
    radio.sample_rate = fs3
except Exception:
    radio.sample_rate(fs3)
    
try:
    x3 = radio.read_samples(N)
except Exception:
    try:
        x3 = radio.read_samples(N)
    except Expection: 
        x3 = radio.capture_data(N)
        
x3 = np.asarray(x3)
print(x3)

t3 = np.arange(N) / fs3

plt.figure()
if np.iscomplexobj(x3): 
    plt.plot(t3[:100], np.real(x3[:100]), label='Re(x)')
    plt.plot(t3[:100], np.imag(x3[:100]), label='Im(x)')
    plt.legend()
else:
    plt.plot(t3[:100],x3[:100])
    
plt.xlabel("Time(s)")
plt.ylabel("Voltage")
plt.title("First 100 samples")
plt.show()

fs_list = np.arange(1.0e6, 3.2e6, 1.0e5)
N = 2048
rows = []

for teehee in fs_list:
    try: 
        radio.sample_rate = teehee 
    except Exception:
        radio.sample_rate(teehee)
        
    for _ in range(2):
        try: 
            lol = np.asarray(radio.read_samples(N))
        except Exception: 
            try:
                lol = np.asarray(radio.read_samples(N))
            except Exception:
                lol = np.asarray(radio.capture_data(N))
                
    f, X, P = compute_spectrum(lol, teehee)
    fpk = peak_frequency(f, P)
    
    rows.append([teehee, fpk])
    print("fs =", teehee, "Hz -> peak =", fpk, "Hz")
    
rows = np.array(rows, dtype=float)

plt.figure()
plt.plot(rows[:,0], rows[:, 1], "o-")
plt.xlabel("Sampling rate fs (Hz)")
plt.ylabel("Measured peak frequency (Hz)")
plt.title("Aliasing behavior: measured peak vs fs")
plt.show()
