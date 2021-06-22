from gtts import gTTS  
from time import sleep
import os
import pygame
import sys

tts=gTTS(text=str(sys.argv[1]), lang='en', slow = False)
filename="audio.mp3"
tts.save(filename)
pygame.mixer.init()
pygame.mixer.music.load("C:/Users/Master/Desktop/onlinequiz-master - Copy/audio.mp3")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
pygame.mixer.quit()
#os.remove(filename)
print("TTS" + sys.argv[1] )
sleep(3)
