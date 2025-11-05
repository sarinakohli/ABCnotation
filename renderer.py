# Renderer module to generate waveforms from ABC files
# references:
# Generating waveforms: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.square.html
# sounddevice for playback: https://python-sounddevice.readthedocs.io/en/0.4.6/
# scipy.io.wavfile for WAV file handling: https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.write.html
# music21 for ABC parsing: https://www.music21.org/music21docs/usersGuide/usersGuide_02_notes.html
# music21 for reapting bars: https://www.music21.org/music21docs/moduleReference/moduleRepeat.html
import numpy as np  # type: ignore
import sounddevice as sd  # type: ignore
from scipy.io.wavfile import write  # type: ignore
from scipy import signal  # type: ignore
from music21 import converter, note, repeat  # type: ignore
from scipy.io.wavfile import read as wav_read  # type: ignore


sampleRate = 44100

notesData = []

# loads ABC file by each note and stores frequency and duration in notesData list


def loadABC(filePath):
    global notesData
    score = converter.parse(filePath)

    try:
        expander = repeat(score)
        score = expander.process()
    except Exception as e:
        print("Warning: could not expand repeats:", e)

    notesData = []
    for n in score .flat.notes:
        if isinstance(n, note.Note):
            freq = n.pitch.frequency
            dur = n.quarterLength * 0.5
            notesData.append((freq, dur))
    print("Loaded", len(notesData), "notes from", filePath)
    return notesData

# applies ADSR envelope to a waveform


def apply_adsr(wave, attack=0.05, decay=0.1, sustain=0.7, release=0.1):
    n = len(wave)
    a = int(n * attack)
    d = int(n * decay)
    r = int(n * release)
    s = n - (a + d + r)
    if s < 0:
        s = 0

    envelope = np.concatenate([
        np.linspace(0, 1, a, endpoint=False),
        np.linspace(1, sustain, d, endpoint=False),
        np.ones(s) * sustain,
        np.linspace(sustain, 0, r, endpoint=True)
    ])

    envelope = np.pad(
        envelope, (0, max(0, n - len(envelope))), mode='constant')[:n]
    return wave * envelope


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

    wave = apply_adsr(wave, attack=0.05, decay=0.1, sustain=0.7, release=0.1)
    return volume * wave

# renders full music piece by concatenating note waveforms, updating the pitch and bpm


def renderMusic(waveform="sine", volume=0.5, bpm=120, pitchShift=0):
    global notesData
    if not notesData:
        raise Exception("No ABC file loaded")

    finalWav = np.array([], dtype=np.float32)

    for freq, dur in notesData:
        shiftedFreq = freq * (2 ** (pitchShift / 12))
        realdur = dur * (120 / bpm)
        if freq == 0:
            noteWav = np.zeros(int(sampleRate * realdur), dtype=np.float32)
        else:
            noteWav = generateWaveform(shiftedFreq, realdur, waveform, volume)
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

# saves the ABC file as a MIDI file using music21


def saveToMidi(filePath, outPath="output.mid"):
    score = converter.parse(filePath)
    score.write('midi', fp=outPath)
    print("MIDI file saved as", outPath)


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

    envelope = np.sin(np.linspace(0, np.pi, n))

    noise = noise / np.max(np.abs(noise))
    noiseyWave = wave + noise * noiseLevel
    return noiseyWave

# mixes the generated waveform with an external WAV file by averaging samples together


def mixWithWav(wave, path):
    rate, extWave = wav_read(path)
    extWave = extWave.astype(np.float32) / 32767.0
    minLen = min(len(wave), len(extWave))
    return 0.5 * (wave[:minLen] + extWave[:minLen])
