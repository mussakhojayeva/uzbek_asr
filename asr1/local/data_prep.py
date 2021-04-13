#!/usr/bin/env python

import sys, argparse, re, os, collections
import pandas as pd
from pathlib import Path
import wave
import contextlib

seed=4

def get_args():
    parser = argparse.ArgumentParser(description="", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--dataset_dir", help="Input data directory", required=True)
    print(' '.join(sys.argv))
    args = parser.parse_args()
    return args


def get_duration(file_path):
    duration = None
    if os.path.exists(file_path) and Path(file_path).stat().st_size > 0:
        with contextlib.closing(wave.open(file_path,'r')) as f:
            frames = f.getnframes()
            if frames>0:
                rate = f.getframerate()
                duration = frames / float(rate)
    return duration if duration else 0

def read_meta(path):
    df = pd.read_csv(path, sep=",")
    folder_name = df['wav_filename'][0].split('/')[0] + '/'
    df['wav_filename'] = df['wav_filename'].apply(lambda x: x.replace(folder_name, ''))
    df.set_index('wav_filename',inplace=True)
    return folder_name, collections.OrderedDict(sorted(df.to_dict()['transcript'].items(), key=lambda x: x[0]))

def prepare_data(dataset_dir, path_root, files):
    total_duration = 0
    wav_format = '-r 16000 -c 1 -b 16 -t wav - downsample |'
    
    with open(path_root + '/text', 'w', encoding="utf-8") as f1, \
    open(path_root + '/utt2spk', 'w', encoding="utf-8") as f2, \
    open(path_root + '/wav.scp', 'w', encoding="utf-8") as f3:
        for path, transcription in files.items():
            filename = os.path.basename(path).replace('.wav', '')
            wav_path = os.path.join(dataset_dir, path)
            total_duration += get_duration(wav_path) 
            f1.write(filename + ' ' + transcription + '\n')
            f2.write(filename + ' ' + filename + '\n')
            f3.write(filename + ' sox ' + wav_path  + ' ' + wav_format +  '\n')   
            
    return total_duration / 3600

def main():
    args = get_args()
    
    dataset_dir = args.dataset_dir
    
    train_folder, train = read_meta(os.path.join(dataset_dir, 'train.csv'))
    dev_folder, dev = read_meta(os.path.join(dataset_dir, 'val.csv'))
    test_folder, test = read_meta(os.path.join(dataset_dir, 'test.csv'))
    
    print('duration of train data:', prepare_data(os.path.join(dataset_dir, train_folder), 'data/train', train))
    print('duration of dev data:', prepare_data(os.path.join(dataset_dir, dev_folder), 'data/dev', dev))
    print('duration of test data:', prepare_data(os.path.join(dataset_dir, test_folder), 'data/test', test))


if __name__ == "__main__":
    main()
