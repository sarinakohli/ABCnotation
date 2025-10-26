# loads abc file, generates waveforms, plays sound and saves to a WAV file
# references:
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from scipy import signal
from music21 import converter, note
from scipy.io.wavfile import read as wav_read

sampleRate = 44100

notesData = []


def loadABC(filePath):
    global notesData
    score = converter.parse(filePath)
    notesData = []
    for n in score .flat.notes:
        if isinstance(n, note.Note):
            freq = n.pitch.frequency
            dur = n.quarterLength * 0.5
            notesData.append((freq, dur))
    print("Loaded", len(notesData), "notes from", filePath)
    return notesData


def generateWaveform(frequency, duration, waveform="sine", volume=0.5):
    t = np.linspace(0, duration, int(sampleRate * duration), False)
    if waveform == "sine":
        wave = np.sin(2 * np.pi * frequency * t)
    elif waveform == "square":
        wave = signal.square(2 * np.pi * frequency * t)
    elif waveform == "triangle":
        wave = signal.sawtooth(2 * np.pi * frequency * t, 0.5)
    elif waveform == "sawtooth":
        wave = signal.sawtooth(2 * np.pi * frequency * t)
    else:
        wave = signal.sawtooth(2 * np.pi * frequency * t)
    return volume * wave


def renderMusic(waveform="sine", volume=0.5, bpm=120, pitchShift=0):
    global notesData
    if not notesData:
        raise Exception("No ABC file loaded")

    finalWav = np.array([], dtype=np.float32)
    for freq, dur in notesData:
        shiftedFreq = freq * (2 ** (pitchShift / 12))
        noteWav = generateWaveform(shiftedFreq, dur, waveform, volume)
        finalWav = np.concatenate((finalWav, noteWav))
    return finalWav


def play(wave):
    sd.play(wave, sampleRate)
    sd.wait()


def saveToWav(wave, filename="output.wav"):
    write(filename, sampleRate, (wave * 32767).astype(np.int16))
    print("Save as", {filename})


def add_noise(wave, noise="white", noiseLevel=0.02):
    noise = np.random.normal(0, noiseLevel, len(wave))
    return wave + noise


def mixWithWav(wave, path):
    rate, extWave = wav_read(path)
    extWave = extWave.astype(np.float32) / 32767.0
    minLen = min(len(wave), len(extWave))
    return 0.5 * (wave[:minLen] + extWave[:minLen])
