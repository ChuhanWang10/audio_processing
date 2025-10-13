import os
import librosa
import shutil
from process_audio import detect_short_audios, get_duration

def read_file_by_lines(filepath):
    with open(filepath, "r") as file:
        lines = [line.rstrip() for line in file]
    return lines

def delete_short_wav_files(dirpath, threshold):
    """Delete the .wav files of which the duration is shorter than a threshold"""

    for root, dirs, files in os.walk(dirpath):
        for file in files:
            if file.lower().endswith('.wav'):
                # print(os.path.relpath(os.path.join(root, file), dirpath))
                wavpath = os.path.join(root, file)
                sampling_rate = librosa.get_samplerate(wavpath)
                duration = get_duration(wavpath,sampling_rate)
                if duration < threshold:
                    print(f"Delete {wavpath}: {duration} seconds")
                    os.remove(wavpath)

def count_files_in_subfolder(root_dirpath, threshold=1):
    """Count the number of files in the lowest level subfolders. Print out the subfolder with less files than a threshold"""

    single_file_subfolder = []
    for dirpath, dirnames, filenames in os.walk(root_dirpath):
        # Skip the root folder itself
        if dirpath != root_dirpath:
            # Find only the lowest-level subfolders
            if not dirnames:
                file_count = len(filenames)
                if file_count <= threshold:
                    print(f"Subfolder: {dirpath}") 
                    print(f"Number of files: {file_count}\n") 
                    single_file_subfolder += dirpath

def copy_wav_files(source_dirpath, destination_dirpath):
    """Copy all .wav files from the source folder to the destination folder."""

    if not os.path.exists(destination_dirpath):
        os.makedirs(destination_dirpath)

    for root, _, files in os.walk(source_dirpath):
        for file in files:
            if file.endswith('.wav'):
                full_filepath = os.path.join(root, file)
                rel_path = os.path.relpath(full_filepath, source_dirpath)
                destination_path = os.path.join(destination_dirpath, rel_path)
                
                # Create the subfolders in the destination folder
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                
                shutil.copy2(full_filepath, destination_path)
                #print(f"Moved: {full_filepath} to {destination_path}")
        
    print(f"All wav files are moved to {destination_dirpath}")

def list_files(dirpath):
    """List all files in a given folder, including those in subdirectories, with relative paths."""

    file_list = []
    for root, _, files in os.walk(dirpath):
        for file in files:
            file_list.append(os.path.relpath(os.path.join(root, file), dirpath))
    return set(file_list)

def count_files(dirpath):
    return len(list_files(dirpath))

def compare_folders(folder1, folder2, target_folder):
    """Compare two folders and return the files that are only in the target folder."""

    files = []
    for dirpath, dirnames, filenames in os.walk(target_folder):
        # Find only the lowest-level subfolders
        if not dirnames:
            for filename in filenames:
                files.append(filename)

    # Check if there are files in the folder
    if files:
       # Get the extension of the first file
       _, extension = os.path.splitext(files[0])
       print(f"The file extension is: {extension}")
    else:
        print("No files found in the folder.")

    files1 = set([file.split(".")[0] for file in list_files(folder1)])
    files2 = set([file.split(".")[0] for file in list_files(folder2)])

    if target_folder == folder1:
        difference = files1 - files2
    elif target_folder == folder2:
        difference = files2 - files1
    
    difference = [file + extension for file in difference]

    print(f"files only exist in the target folder: {difference}")

    return difference

def remove_files(files_to_remove, dirpath):
    '''
    files_to_remove: a list of filenames
    dirpath: path to the directory where the files need to be removed
    '''

    # Remove the files that are only in folder_to_clean
    for filename in files_to_remove:
        filepath = os.path.join(dirpath, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Deleted: {filepath}")
        else:
            print(f"File not found (skipped): {filepath}")
    


def compare_folders_and_remove(folder1, folder2, folder_to_clean):
    """Compare two folders and remove files from folder_to_clean that are not in the other folder."""

    files1 = list_files(folder1)
    files2 = list_files(folder2)

    if folder_to_clean == folder1:
        files_to_remove = files1 - files2
    elif folder_to_clean == folder2:
        files_to_remove = files2 - files1
    else:
        raise ValueError("folder_to_clean must be either folder1 or folder2.")

    # Remove the files that are only in folder_to_clean
    for file in files_to_remove:
        file_to_delete = os.path.join(folder_to_clean, file)
        if os.path.exists(file_to_delete):
            os.remove(file_to_delete)
            print(f"Deleted: {file_to_delete}")
        else:
            print(f"File not found (skipped): {file_to_delete}")

if __name__ == '__main__':
    # folder_path = "/home/chuwan/data/LibriTTS_R_16k/train-clean-100"
    # folder_path = "/home/chuwan/experiments/knn-vc/data/rsvc_real/rsvc_real_16k"
    # detect_short_audios(folder_path, threshold=1)
    # count_files_in_subfolder(folder_path, threshold=1)

    # source_dirpath = "/opt/share/common/db/audio_corpora/LibriTTS_R"
    # destination_dirpath = "/home/chuwan/data/LibriTTS_R_24k"
    # copy_wav_files(source_dirpath,destination_dirpath)

    # folder1 = "/home/chuwan/data/LibriTTS_R_24k"
    # folder2 = "/home/chuwan/experiments/knn-vc/prematched/LibriTTS_R_16k"
    # folder_to_clean = folder1  
    # compare_folders_and_remove(folder1, folder2, folder_to_clean)
    # print(count_files(folder1), count_files(folder2))

    # num_cpus = os.cpu_count()
    # print(f"Number of CPUs: {num_cpus}")

    folder1 = "/home/chuwan/experiments/knn_vc_all_branches/enhanced_features/knn-vc/prematched/LibriTTS_R_rsvc_real_L6"
    folder2 = "/home/chuwan/experiments/knn_vc_all_branches/enhanced_features/knn-vc/prematched/LibriTTS_R_rsvc_real_L6_21"
    print(count_files(folder1), count_files(folder2))
    diff = compare_folders(folder1, folder2, target_folder=folder1)
    #remove_files(files_to_remove=diff, dirpath=folder1)

    # folder_path = "/home/chuwan/data/LibriTTS_R_16k/raw"
    # print(count_files(folder_path))
