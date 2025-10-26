# loads abc file, generates waveforms, plays sound and saves to a WAV file
# references:
# Generating waveforms: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.square.html
# sounddevice for playback: https://python-sounddevice.readthedocs.io/en/0.4.6/
# scipy.io.wavfile for WAV file handling: https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.write.html
# music21 for ABC parsing: https://www.music21.org/music21docs/usersGuide/usersGuide_02_notes.html
import numpy as np  # type: ignore
import sounddevice as sd  # type: ignore
from scipy.io.wavfile import write  # type: ignore
from scipy import signal  # type: ignore
from music21 import converter, note  # type: ignore
from scipy.io.wavfile import read as wav_read  # type: ignore

sampleRate = 44100

notesData = []

# loads ABC file by each note and stores frequency and duration in notesData list


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

# generates waveform for a single note


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

# renders full music piece by concatenating note waveforms


def renderMusic(waveform="sine", volume=0.5, pitchShift=0):
    global notesData
    if not notesData:
        raise Exception("No ABC file loaded")

    finalWav = np.array([], dtype=np.float32)
    for freq, dur in notesData:
        shiftedFreq = freq * (2 ** (pitchShift / 12))
        noteWav = generateWaveform(shiftedFreq, dur, waveform, volume)
        finalWav = np.concatenate((finalWav, noteWav))
    return finalWav

# plays the generated waveform


def play(wave):
    sd.play(wave, sampleRate)
    sd.wait()

# saves the generated waveform to a WAV file using scipy.io.wavfile


def saveToWav(wave, filename="output.wav"):
    write(filename, sampleRate, (wave * 32767).astype(np.int16))
    print("Save as", {filename})

# adds noise to the waveform for white noise, pink noise, or brown noise


def add_noise(wave, noiseType="pink", noiseLevel=0.08):
    n = len(wave)
    if noiseType == "white":
        noise = np.random.normal(0, 1, n)
    elif noiseType == "pink":
        uneven = n % 2
        X = np.random.randn(n // 2 + 1 + uneven) + 1j * \
            np.random.randn(n // 2 + 1 + uneven)
        S = np.sqrt(np.arange(len(X)) + 1.)
        y = (np.fft.irfft(X / S)).real
        if uneven:
            y = y[:-1]
        y = y / np.max(np.abs(y))
        noise = y
    elif noiseType == "brown":
        white = np.random.normal(0, 1, n)
        noise = np.cumsum(white)
        noise = noise / np.max(np.abs(noise))
    else:
        raise ValueError("Unsupported noise type")

    noise = noise / np.max(np.abs(noise))
    noiseyWave = wave + noise * noiseLevel
    return noiseyWave

# mixes the generated waveform with an external WAV file by averaging samples together


def mixWithWav(wave, path):
    rate, extWave = wav_read(path)
    extWave = extWave.astype(np.float32) / 32767.0
    minLen = min(len(wave), len(extWave))
    return 0.5 * (wave[:minLen] + extWave[:minLen])
