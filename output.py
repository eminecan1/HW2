import numpy as np
from scipy.io.wavfile import read
from scipy.fft import fft

fs, data = read("output.wav")

data = data / np.max(np.abs(data))

duration = 0.04
window_size = int(fs * duration)

characters = list("ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ ")

low_freqs = np.linspace(300, 900, 6)
high_freqs = np.linspace(1000, 2000, 5)

freq_map = {}
reverse_map = {}

index = 0
for f1 in low_freqs:
    for f2 in high_freqs:
        if index < len(characters):
            freq_map[characters[index]] = (f1, f2)
            reverse_map[(round(f1), round(f2))] = characters[index]
            index += 1

def find_closest(freq, freq_list):
    return min(freq_list, key=lambda x: abs(x - freq))

decoded_text = ""

for i in range(0, len(data), window_size):
    segment = data[i:i+window_size]
    
    if len(segment) < window_size:
        continue
    
    # Apply Hamming window
    segment = segment * np.hamming(len(segment))
    
    spectrum = np.abs(fft(segment))
    freqs = np.fft.fftfreq(len(segment), 1/fs)
    
    # Only positive frequencies
    positive_freqs = freqs[:len(freqs)//2]
    positive_spectrum = spectrum[:len(spectrum)//2]
    
    # Find 2 highest peaks
    peak_indices = positive_spectrum.argsort()[-2:]
    peak_freqs = sorted(positive_freqs[peak_indices])
    
    f1 = find_closest(peak_freqs[0], low_freqs)
    f2 = find_closest(peak_freqs[1], high_freqs)
    
    key = (round(f1), round(f2))
    
    if key in reverse_map:
        decoded_text += reverse_map[key]

print("Decoded Text:", decoded_text)
