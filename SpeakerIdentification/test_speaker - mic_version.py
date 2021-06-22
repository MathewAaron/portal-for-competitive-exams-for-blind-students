#speaker identification for audio recorded using microphone
import os
import pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
from speakerfeatures import extract_features
import warnings
warnings.filterwarnings("ignore")
import time
import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 3  # Duration of recording

#path to training data
source   = "development_set\\"   

modelpath = "speaker_models\\"


gmm_files = [os.path.join(modelpath,fname) for fname in 
              os.listdir(modelpath) if fname.endswith('.gmm')]

#Load the Gaussian gender Models
models    = [cPickle.load(open(fname,'rb')) for fname in gmm_files]
speakers   = [fname.split("\\")[-1].split(".gmm")[0] for fname 
              in gmm_files]
speakers.append('noisy/new speaker')
#length = len(speakers)

# Recird audio from microphone
print('Recording audio')
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()  # Wait until recording is finished
#write('output.wav', fs, myrecording)  # Save as WAV file

vector   = extract_features(myrecording,fs) #extract features
    
log_likelihood = np.zeros(len(models)) 
    
for i in range(len(models)):
    gmm    = models[i]         #checking with each model one by one
    scores = np.array(gmm.score(vector))
    log_likelihood[i] = scores.sum()

predicted = np.argmax(log_likelihood)
print(log_likelihood)
print("\tdetected as - ", speakers[predicted])


        
