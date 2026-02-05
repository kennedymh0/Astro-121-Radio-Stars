import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, stats
import ugradio.dft as dft
from src import plotting_stuff, analysis, acquiring_data


plotting_stuff.setup_plot_style()

path = "/home/radiopi/Astro-121-Radio-Stars/lab1/test_ng__20260204_170343"
noise_file = os.listdir(path)


