import ugradio
import ugradio.sdr
import ugradio.dft
import numpy as np
import astropy
import matplotlib.pyplot as plt
radio = ugradio.sdr.SDR(device_index=0)
fs = 2.4e6
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