#train_models.py

import pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture as GM 
from speakerfeatures import extract_features
import warnings
warnings.filterwarnings("ignore")
import joblib
import os
import warnings
warnings.filterwarnings("ignore")

#path to training data
source   = "development_set\\"   

#path where training speakers will be saved
dest = "speaker_models\\"
train_file = "development_set_enroll.txt"        

file_paths = open(train_file,'r')

count = 1

# Extracting features for each speaker (4 files for each speaker)
features = np.asarray(())
for path in file_paths:    
    path = path.strip()   
    print(path)
    
    # read the audio
    sr,audio = read(source + path)
    
    # extract 40 dimensional MFCC & delta MFCC features
    vector   = extract_features(audio,sr)
    
    if features.size == 0:
        features = vector
    else:
        features = np.vstack((features, vector))
    # when features of 3 files of speaker are concatenated, then do model training
    if count == 3:    
        gmm = GM(n_components = 16,  covariance_type='diag',n_init = 3)
        gmm.fit(features)
        
        # dumping the trained gaussian model
        splt_char = "\\"
        temp = path.split(splt_char)
        #res = splt_char.join(temp[:2]), splt_char.join(temp[2:])
        path = 'A:\VIT_Projects\Major Project\speaker_models'
        file = temp[0]+".gmm"
        #file = path+".gmm"
        f = open(os.path.join(path, file), 'wb')
        cPickle.dump(gmm,f,-1)
        #joblib.dump(gmm,picklefile)
        f.close()
        print('+ modeling completed for speaker:',file," with data point = ",features.shape )   
        features = np.asarray(())
        count = 0
    count = count + 1
    
