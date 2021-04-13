
## Setup and Requiremnts 
After succesfull installation of ESPnet & Kaldi, go to `uzbek_asr/asr1` folder and create links to the dependencies:
```
ln -s ../../../tools/kaldi/egs/wsj/s5/steps steps
ln -s ../../../tools/kaldi/egs/wsj/s5/utils utils
```
The directory for running the experiments (`uzbek_asr/<exp-name`) can be created by running the following script:

```
./setup_experiment.sh <exp-name>
```

## Training

To train the models, run the script `./run.sh` inside `uzbek_asr/<exp-name>/` folder.

## Inference
To decode a single audio, specify paths to the following files inside `recog_wav.sh` script:
```
lang_model= path to rnnlm.model.best
cmvn= path to cmvn.ark for example data/train/cmvn.ark
recog_model= path to e2e model, in case of transformer: model.last10.avg.best 
```
Then, run the following script:
```
./recog_wav.sh <path-to-audio-file>
```
