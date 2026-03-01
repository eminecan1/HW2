import numpy as np
from scipy.io.wavfile import write

# Sampling rate
fs = 44100  

# Character duration (40 ms)
duration = 0.04  

# Turkish alphabet + space
characters = list("ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ ")  

# Frequency pools
low_freqs = np.linspace(300, 900, 6)
high_freqs = np.linspace(1000, 2000, 5)

# Create frequency pairs (30 characters)
freq_map = {}
index = 0
for f1 in low_freqs:
    for f2 in high_freqs:
        if index < len(characters):
            freq_map[characters[index]] = (f1, f2)
            index += 1

def generate_tone(f1, f2, duration, fs):
    t = np.linspace(0, duration, int(fs*duration), endpoint=False)
    tone = np.sin(2*np.pi*f1*t) + np.sin(2*np.pi*f2*t)
    return tone

def encode_text(text):
    signal = np.array([])
    for char in text.upper():
        if char in freq_map:
            f1, f2 = freq_map[char]
            tone = generate_tone(f1, f2, duration, fs)
            signal = np.concatenate((signal, tone))
    return signal

# Example text
text = "MERHABA DUNYA"

encoded_signal = encode_text(text)

# Normalize
encoded_signal = encoded_signal / np.max(np.abs(encoded_signal))

# Save file
write("output.wav", fs, (encoded_signal * 32767).astype(np.int16))

print("Encoding completed. output.wav created.")
