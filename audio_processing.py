import os
import wave
import numpy as np
from scipy.io.wavfile import read, write
import soundfile as sf
import librosa
from matplotlib import pyplot as plt
import scipy

# obtain the sampling rate of a wav
def get_sampling_rate(filename):
    with wave.open(filename, 'rb') as wav_file:
        sampling_rate = wav_file.getframerate()
        return sampling_rate

# load wav via librosa, scipy or soundfile    
def load_wav_librosa(wavpath):
    # return sampling_rate, wav
    wav, sampling_rate = librosa.core.load(wavpath, sr=None)
    return wav, sampling_rate

def load_wav_scipy(wavpath):
    # return sampling_rate, wav
    MAX_WAV_VALUE = 32768.0 #2**15
    sampling_rate, wav = scipy.io.wavfile.read(wavpath)
    wav = wav / MAX_WAV_VALUE
    return sampling_rate, wav

def load_wav_soundfile(wavpath):
    # return wav, sampling_rate
    wav, sampling_rate = sf.read(wavpath)
    return wav, sampling_rate

def get_duration(wavpath, sampling_rate):
    return librosa.get_duration(filename=wavpath, sr=sampling_rate)

def detect_long_pauses(wavpath, threshold, pause_duration_threshold):
    # Load the audio file
    audio_signal, sample_rate = librosa.load(wavpath, sr=None)

    # Calculate the total length of the audio
    total_length = librosa.get_duration(audio_signal, sample_rate)

    # Calculate energy or amplitude
    window_size = int(sample_rate * 1)  # 1 second window 
    stride = int(sample_rate * 0.1)  # 0.1 second stride 

    energies = [
        np.sum(audio_signal[i:i + window_size] ** 2)
        for i in range(0, len(audio_signal) - window_size, stride)
    ]

    # Detect pauses larger than a certain duration
    pauses = []
    in_pause = False
    pause_start = 0

    for i, energy in enumerate(energies):
        if energy <= threshold and not in_pause:
            in_pause = True
            pause_start = i * stride / sample_rate
        elif energy > threshold and in_pause:
            pause_end = i * stride / sample_rate
            pause_duration = pause_end - pause_start
            if pause_duration > pause_duration_threshold:
                pauses.append((pause_start, pause_duration))
                in_pause = False
                
    return total_length, pauses
