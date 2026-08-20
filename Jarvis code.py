# -*- coding: utf-8 -*-

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from pathlib import Path
import pyttsx3
import sounddevice as sd
import soundfile as sf
from faster_whisper import WhisperModel

engine = pyttsx3.init()
model = WhisperModel("tiny", device = "cpu", compute_type = "int8")

def retrieval(route):
    d = {}
    folder = Path(route)
    for p in folder.rglob("*.md"):
        print(p)
        d[str(p.relative_to(folder))] = p.read_text(encoding='utf-8')
    return d


def fetch_file(question: str, d: dict):
    L=[]
    stopwords = {"what", "the", "is", "my", "are", "a", "of", "to", "how", "do", "i"}
    question = question.lower()
    q = question.split()
    Q = [w for w in q if w not in stopwords]
    for names, text in d.items():
        if len(text) == 0:
            score = 0
            L.append((names, score))
            
        else:
            score = (sum(text.lower().count(w) for w in Q) + sum(3*names.lower().count(w) for w in Q)) / len(text)
            L.append((names, score))
    best = sorted(L, key= lambda t: t[-1], reverse = True)
    winners = best[:5]
    if best[0][-1] == 0:
        return []
    return winners

    
def speak(text: str):
    
    engine.say(text)
    engine.runAndWait()
    
def record(duration = 5):
    audio = sd.rec(duration*16000, samplerate = 16000, channels = 1)
    sd.wait()
    sf.write("test.wav", audio, 16000)
    print(audio.max(), audio.min())
    return audio

def transcribe(file):
    segments, info = model.transcribe(file)
    for s in segments:
        print(s.text)


