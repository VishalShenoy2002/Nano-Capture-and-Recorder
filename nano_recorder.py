from pyaudio import PyAudio
from pyaudio import paInt32
import wave

import speech_recognition as sr

import keyboard
import datetime
import os
import sys

import argparse

RATE=44100
BUFFER=2048
FORMAT=paInt32
CHANNELS=2

PATH=os.path.join(os.getcwd(),"recordings")
try:
    os.makedirs(PATH)
except FileExistsError:
    pass

class Recorder:

    def __init__(self):
        self.audio=PyAudio()
        self.stream=self.audio.open(RATE, CHANNELS, FORMAT,input=True)
        self.frames=[]

    def record(self):
        print("Press 'T' or 't' to stop recording")
        try:
            while True:
                data=self.stream.read(BUFFER)
                self.frames.append(data)

                if keyboard.is_pressed("t") or keyboard.is_pressed("T"):
                    raise KeyboardInterrupt

        except KeyboardInterrupt:
            self.stream.close()
            self.audio.terminate()

        timestamp=datetime.datetime.today().now().strftime("%d%m%y_%H%M%S")
        filename=os.path.join(PATH,f"Recording_{timestamp}.wav")

        with wave.open(filename,"wb") as audiofile:
            audiofile.setnchannels(CHANNELS)
            audiofile.setsampwidth(self.audio.get_sample_size(FORMAT))
            audiofile.setframerate(RATE)
        

            audiofile.writeframes(b''.join(self.frames))
            audiofile.close()

        return filename

    def recordAndTranscript(self):
        file=self.record()

        recogniser=sr.Recognizer()
        with sr.AudioFile(file) as audiofile:
            audio=recogniser.record(audiofile)
            data=recogniser.recognize_google(audio)

        filename=file.split('.')[0]
        with open(f"{filename}_transcript.txt","w") as f:
            f.write(data)
            f.close()

    def generateTranscript(self,filename:str):

        if not filename.endswith(".wav"):
            raise TypeError("The recording should be a wave file (*.WAV or *.wav)")
        else:
            file=filename
            recogniser=sr.Recognizer()
            with sr.AudioFile(file) as audiofile:
                audio=recogniser.record(audiofile)
                data=recogniser.recognize_google(audio)

            filename=file.split('.')[0]
            with open(f"{filename}_transcript.txt","w") as f:
                f.write(data)
                f.close()

def listRecordings():
    files=[file for file in os.listdir(PATH) if file.endswith(".wav")]
    print("RECORDINGS")
    print("--"*20)
    for index,file in enumerate(files,start=1):
        print(f"[{index}]  {file}")

def listTranscripts():
    files=[file for file in os.listdir(PATH) if file.endswith(".txt")]
    print("TRANSCRIPTS")
    print("--"*20)
    for index,file in enumerate(files,start=1):
        print(f"[{index}]  {file}")


def createParser():

    parser=argparse.ArgumentParser()

    parser.add_argument("--record",action="store_true",help="Records the audio.")
    parser.add_argument("--record-with-transcript",action="store_true",help="Records the audio and creates a transcript for the same.")
    parser.add_argument("--list-recordings",action="store_true",help="Lists all the recording files")
    parser.add_argument("--list-transcripts",action="store_true",help="Lists all the transcript files")
    parser.add_argument("--generate-transcript",action="store",help="Generates a transcript for a pre-recorded (.wav) file")
    args=parser.parse_args()

    return args



if __name__ =="__main__":
    rec=Recorder()
    args=createParser()
    if args.record == True and args.record_with_transcript == True:
        sys.exit("Recording and Recording with transcript can't be done together.")

    elif args.generate_transcript == True and (args.record_with_transcript == True or args.record == True):
        sys.exit("Generating transcript should be done separately.") 

    else:
        if args.record == True:
            rec.record()

        elif args.record_with_transcript == True:
            rec.recordAndTranscript()

        elif args.list_recordings == True:
            listRecordings()

        elif bool(args.generate_transcript)== True:
            rec.generateTranscript(args.generate_transcript)

        elif args.list_transcripts ==True:
            listTranscripts()

        else:
            sys.exit("No Such option exists. Please Type madhura --help to see option")
        
    