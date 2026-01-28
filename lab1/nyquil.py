import ugradio 
import ugradio.sdr
import ugradio.dft
import numpy as np
import astropy
import matplotlib.pyplot as plt
radio = ugradio.sdr.SDR(device_index=0)

fs1 = 3.2e6
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
    plt.plot(t1[:25], np.real(x1[:25]), label='Re(x)')
    plt.plot(t1[:25], np.imag(x1[:25]), label='Im(x)')
    plt.legend()
else:
    plt.plot(t1[:100],x1[:100])
    
plt.xlabel("Time(s)")
plt.ylabel("Voltage")
plt.title("First 100 samples")
plt.show()