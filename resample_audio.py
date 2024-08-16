import os
import sys

import numpy as np
from scipy.io import wavfile
from tqdm import tqdm
import librosa
import soundfile as sf

sys.path.append("../")

def get_sampling_rate(filepath):
    if filepath.endswith('.wav'):
        _, sr = librosa.load(filepath, sr=None)
    print(f"The sampling rate of this wavfile is {sr}")
    return sr

# resample a .wav file
def load_and_resample(filepath, new_sr):
    y, sr = librosa.load(filepath, sr=None)
    if new_sr != sr:
        y = librosa.resample(y, orig_sr=sr, target_sr=new_sr)
        y = np.clip(y, -1.0, 32767.0/32768.0)
    return y

def batch_resample(source_folder, target_folder, target_sr=16000):
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith('.wav'):
                file_path = os.path.join(root, file)
                y_float = load_and_resample(file_path, target_sr)
                y_int = (y_float*32768.).astype('int16')
                
                # Determine the target file path
                relative_path = os.path.relpath(file_path, source_folder)
                target_file_path = os.path.join(target_folder, relative_path)
                
                # Ensure the target directory exists
                target_dir = os.path.dirname(target_file_path)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                
                # Save the resampled file
                sf.write(target_file_path, y_int, target_sr)
                print(f"Resampled {file_path} to {target_file_path} with sampling rate {target_sr}")

if __name__ == '__main__':
    source_folder = '/home/chuwan/experiments/knn-vc/zsvc_testing/vctk'  # Change to your source folder path
    target_folder = '/home/chuwan/experiments/NeuCoSVC/test_data/vctk_24k'  # Change to your target folder path
    sr = 24000 # Change to your target sampling rate

    # Resample all .wav files in the source folder and save them to the target folder
    batch_resample(source_folder, target_folder, sr)




