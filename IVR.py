from sys import byteorder
from array import array
from struct import pack
import msvcrt

import pyaudio
import wave
from gtts import gTTS
import vlc
import time
import MySQLdb


THRESHOLD = 30000
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD

def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

def record():
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the 
    start and end, and pads with 0.5 seconds of 
    blank sound to make sure VLC et al can play 
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    r = array('h')

    while 1:
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)

        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True
            print "Sound Detected"

        if snd_started and num_silent > 30:
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return sample_width, r

def sound_test():
        record_to_file('demo.wav')
        return 1

def rec():
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "file.wav"
     
    audio = pyaudio.PyAudio()
     
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print "recording..."
    frames = []
     
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print "finished recording"
     
     
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
     
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    
    
if __name__ == '__main__':
    test_value = sound_test()
    if test_value == 1:
        p = vlc.MediaPlayer("sound/hello.mp3")
        p.play()
        time.sleep(5)
                
        print "Enter your department"
        p = vlc.MediaPlayer("sound/dep.mp3")
        p.play()
        c=input()
        if c==1:
            dep='civil'
        elif c==2:
            dep='cs'
        elif c==3:
            dep='eee'
        elif c==4:
            dep='ec'
        elif c==5:
            dep='mech'
        p = vlc.MediaPlayer("sound/sem.mp3")
        p.play()
        sem=input()
        p = vlc.MediaPlayer("sound/batch.mp3")
        p.play()
        b=input()
        if b==1:
            batch='a'
        elif b==2:
            batch='b'
        p = vlc.MediaPlayer("sound/roll.mp3")
        p.play()
        rollno=input()

        print dep
        print sem
        print batch 
        db = MySQLdb.connect('localhost',"testuser","test123","mace")
        c=db.cursor()
        q="select name from test where rollno ='%d'"% (rollno)
        c.execute(q)
        data=c.fetchall()
        for row in data:
            name = row[0]
        print "welcome " + name
        tts = gTTS("hello ,"+name+"."+"Welcome", lang='en')
        tts.save("s.mp3")
        p = vlc.MediaPlayer("s.mp3")
        p.play()
        msvcrt.getch()


    
    
        
        
    
    
    
