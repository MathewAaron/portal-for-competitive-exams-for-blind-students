from django.http.response import HttpResponse
from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from teacher import models as TMODEL
#Libraries for TTS
from gtts import gTTS  
from time import sleep
import os
import pygame
from playsound import playsound
#Libraries for STT
import speech_recognition as sr



tr_mins = 180
tr_secs = 0

#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')

def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    }
    return render(request,'student/student_dashboard.html',context=dict)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_exam.html',{'courses':courses})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    #text2speech.speak("Exam name is " + str(course) + ".Total number of Questions are" + str(total_questions) + ".Total Marks are" + str(total_marks))
    return render(request,'student/take_exam.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks})
    
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    questions=QMODEL.Question.objects.all().filter(course=course)
    if request.method=='POST':
        pass
    response= render(request,'student/start_exam.html',{'course':course,'questions':questions,'time_mins':tr_mins,'time_secs':tr_secs})
    response.set_cookie('course_id',course.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        
        total_marks=0
        questions=QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        result.save()

        return HttpResponseRedirect('view-result')


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def score(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'student/check_marks.html',{'results':results})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/view_result.html',{'courses':courses})
    

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'student/check_marks.html',{'results':results})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_marks.html',{'courses':courses})

def speak(request):

    
    if request.method == 'POST':
        #print("This is the speak function")
        text = request.POST.get("mydata")
        tts=gTTS(text=str(text), lang='en', slow = False)
        filename="audio.mp3"
        tts.save(filename)
        pygame.mixer.init()
        pygame.mixer.music.load("C:/Users/Master/Desktop/onlinequiz-master - Copy/audio.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
        return HttpResponse(text)
    if request.method == 'GET':
        return HttpResponse('Request method was get')


def SpeechRecog(request):
    if request.method == "GET":
        render("Speech Recog Get")
    if request.method == "POST":
        sample_rate = 44100
        #Chunk is like a buffer. It stores 2048 samples (bytes of data)
        #here.
        #it is advisable to use powers of 2 such as 1024 or 2048
        chunk_size = 1024
        r = sr.Recognizer()
        mic= sr.Microphone(device_index=1)
        with sr.Microphone(device_index = 1, sample_rate = sample_rate, chunk_size = chunk_size) as source:
            r.adjust_for_ambient_noise(source)
            print ("Say Something")
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio,language="en-US")
                print ("you said: " + text)
                return HttpResponse(text)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return HttpResponse()

#Libraries for speaker identification
import pickle as cPickle
import numpy as np
from scipy.io.wavfile import read
import warnings
warnings.filterwarnings("ignore")
import time
import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf

import numpy as np
from sklearn import preprocessing
import python_speech_features as mfcc

def calculate_delta(array):
    """Calculate and returns the delta of given feature vector matrix"""

    rows,cols = array.shape
    deltas = np.zeros((rows,20))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i-j < 0:
                first = 0
            else:
                first = i-j
            if i+j > rows -1:
                second = rows -1
            else:
                second = i+j
            index.append((second,first))
            j+=1
        deltas[i] = ( array[index[0][0]]-array[index[0][1]] + (2 * (array[index[1][0]]-array[index[1][1]])) ) / 10
    return deltas

def extract_features(audio,rate):
    """extract 20 dim mfcc features from an audio, performs CMS and combines 
    delta to make it 40 dim feature vector"""    
    
    mfcc_feat = mfcc.mfcc(audio,rate, 0.025, 0.01,20,nfft=2048,appendEnergy = True)
    
    mfcc_feat = preprocessing.scale(mfcc_feat)
    delta = calculate_delta(mfcc_feat)
    combined = np.hstack((mfcc_feat,delta)) 
    return combined

def optionselect(request):
    if request.method == "POST":
        chunk = 1024
        fs = 44100  # Sample rate
        seconds = 3

        print('Recording audio')
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        print(type(myrecording[0][0]))
        sd.wait()  # Wait until recording is finished
        sf.write('output.wav', myrecording,fs)  # Save as WAV file
        #path to training data
        source   = "C:/Users/Master/Desktop/onlinequiz-master - Copy/SpeakerIdentification/development_set/"   
        modelpath = "C:/Users/Master/Desktop/onlinequiz-master - Copy/SpeakerIdentification/speaker_models/"
        gmm_files = [os.path.join(modelpath,fname) for fname in os.listdir(modelpath) if fname.endswith('.gmm')]
        #Load the Gaussian gender Models
        models    = [cPickle.load(open(fname,'rb')) for fname in gmm_files]
        speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname 
                    in gmm_files]
        speakers.append('noisy/new speaker')

        vector   = extract_features(myrecording,fs) #extract features
            
        log_likelihood = np.zeros(len(models)) 
            
        for i in range(len(models)):
            gmm    = models[i]         #checking with each model one by one
            scores = np.array(gmm.score(vector))
            log_likelihood[i] = scores.sum()

        predicted = np.argmax(log_likelihood)
        print(log_likelihood)
        print("\tdetected as - ", speakers[predicted])

        r = sr.Recognizer()
        with sr.AudioFile("output.wav") as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)
            try:
                text = r.recognize_google(audio,language="en-US")
                print ("OPselect you said: " + text)
                return HttpResponse(text)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return HttpResponse()




def speakscore(request):
    if request.method == 'POST':
        time.sleep(3)
        text = request.POST.get("mydata")
        tts=gTTS(text=str(text), lang='en', slow = False)
        filename="audio.mp3"
        tts.save(filename)
        pygame.mixer.init()
        pygame.mixer.music.load("C:/Users/Master/Desktop/onlinequiz-master - Copy/audio.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
        return HttpResponse(text)
    if request.method == 'GET':
        return HttpResponse('Request method was get')


