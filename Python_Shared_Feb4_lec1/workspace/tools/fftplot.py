'''
fftplot.py
Custom fft and plotting libraries

Copyright (C) 2018-2020 C. Daniel Boschen

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above
copyright notice, this list of conditions and the following
disclaimer in the documentation and/or other materials provided
with the distribution.

3. The name of the author may not be used to endorse or promote
products derived from this software without specific prior
written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS
OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import numpy as np
import scipy.fftpack as fft
import scipy.signal as sig
import matplotlib.pyplot as plt

def winfft(vec, fs=1., full_scale=1., beta=12., n_samp = None):
    """
    Returns Kaiser windowed fft with proper scaling of tones

    Dan Boschen 12/2/2018    

    Parameters
    ----------
    
    vec : 1d list-like object
        input time domain signal
        
    fs: float, optional
        Sampling rate in Hz, default = 1.0
        
    full_scale: float, optional 
        normalization for full scale, default = 1.0 (0 dB)
        
    beta: float, optional
        Kaiser beta, default = 12.0 
        
    n_samp: integer, optional
        Number of samples, if longer will zero pad vec

    Returns
    -------
    
    faxis: ndarray, float
        Frequency axis
    
    fout: ndarray, complex float
        scaled frequency output values

    """
    
   
    # length of input     
    input_len = np.shape(vec)[0]

    if n_samp == None:
        n_samp = input_len
    elif n_samp < input_len:
        vec = vec[:n_samp]
        
    # only window data, not zero padded signal:
    win_len = input_len if n_samp > input_len else n_samp 
    
    win = sig.kaiser(win_len, beta)
    winscale = np.sum(win)
    
    win_data = win * vec 
    
    # scaled fft
    fout = 1./(winscale*full_scale) * fft.fft(win_data, n_samp)
    
    # fftshift
    fout = fft.fftshift(fout)
    
    # create frequency axis
    faxis = np.array(range(n_samp)) * fs / n_samp - fs / 2

    return faxis, fout


def plot_spectrum(faxis, fout, drange = 150):
    """
    Plots frequency spectrum in dB
    
    Must enter plt.figure() before calling (to allow for 
    plotting over an existing plot)
    
    Dan Boschen 12/2/2018
    
    Parameters
    ----------    
    
    faxis: ndarray, float
        Frequency axis
    
    fout: ndarray, complex float
        scaled frequency output values
        
    drange: float, optional
        dynamic range, default = 150
        
    Returns:
    --------
    
    None
    """

    # avoids log of 0 errors
    def _safelog(x, minval=1e-10): return np.log10(x.clip(min=minval))


    # scaling of frequency axis

    if (faxis[-1] >= 1000) and (faxis[-1] < 1e6):
        plt.plot(faxis/1000, 20 * _safelog(np.abs(fout)))
        plt.axis([faxis[0]/1000, faxis[-1]/1000, -drange, 0])
        plt.xlabel('Frequency [KHz]')   		
    elif faxis[-1] > 1e6:
        plt.plot(faxis/1e6, 20 * _safelog(np.abs(fout)))
        plt.axis([faxis[0]/1e6, faxis[-1]/1e6, -drange, 0])
        plt.xlabel('Frequency [MHz]')
    elif faxis[-1] > 1e9:
        plt.plot(faxis/1e9, 20 * _safelog(np.abs(fout)))
        plt.axis([faxis[0]/1e9, faxis[-1]/1e9, -drange, 0])
        plt.xlabel('Frequency [GHz]')  
    else:
        plt.plot(faxis, 20 * _safelog(np.abs(fout)))
        plt.axis([faxis[0], faxis[-1], -drange, 0])
        plt.xlabel('Frequency [Hz]')
        
    plt.ylabel('Magnitude [dBFS]')
    plt.grid(True)
