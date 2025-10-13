import os
from tqdm import tqdm
from pydub import AudioSegment

def convert_flac_to_wav(input_flac: str, output_wav: str):
    # Load the .flac file
    audio = AudioSegment.from_file(input_flac, format="flac")

    output_dir = os.path.dirname(output_wav)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Export as .wav
    audio.export(output_wav, format="wav")
    #print(f"Conversion complete: {input_flac} -> {output_wav}")


def batch_conversion(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Collect all .flac files
    flac_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.flac'):
                flac_files.append(os.path.join(root, file))

    # Iterate over flac files with tqdm progress bar
    for flacpath in tqdm(flac_files, desc="Converting files", unit="file"):
        relative_path = os.path.relpath(flacpath, input_dir)
        wavpath = os.path.join(output_dir, relative_path).replace(".flac", ".wav")
        convert_flac_to_wav(flacpath, wavpath)
    
    print(f"All conversions are finished and saved in {output_dir}")

if __name__ == '__main__':
    # input_flac = "/opt/share/common/db/audio_corpora/LibriSpeech_16k/test_clean_100/test-clean/61/70968/61-70968-0000.flac"
    # output_wav = "/home/chuwan/experiments/audio_processing/output_file.wav"
    #convert_flac_to_wav(input_flac, output_wav)

    input_dir = "/mnt/lore/research/data/audio_corpora/Librispeech/flac"
    output_dir = "/mnt/lore/research/data/audio_corpora/Librispeech/wav"
    batch_conversion(input_dir, output_dir)
