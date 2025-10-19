import os
from pickle import TRUE
import sys
from dataclasses import dataclass
from typing import List, Optional

defaultBpm = 120
sampleRate = 44100
waveForms = ['sine', 'square', 'sawtooth', 'triangle']
noiseType = ['white', 'pink', 'brown']


@dataclass
class noteEvent:
    freq: Optional[float]
    duration: float
    velocity: float = 0.1


class SongRenderer:
    def __init__(self):
        self.waveform = 'sine'
        self.loudness = 0.8
        self.abc_path = None
        self.bpm = defaultBpm
        self.pitchShift = 0
        self.noiseTpye = None
        self.noiseLevel = 0.0
        self.mixWavPatch = None
        self.adsr = (0.01, 0.05, 0.8, 0.08)
        self.currentEvents: List[noteEvent] = []
        self.headers = {}


renderer = SongRenderer()


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def option1():
    cls()
    print("Select waveform:")
    input()


def option2():
    cls()
    print("Enter loudness:")
    input()


def option3():
    cls()
    print("Enter ABC file path:")
    i = input()
    try:
        renderer.load_abc(i)
    except Exception as e:
        print("failed to load ABC:", e)


def option4():
    cls()
    print("Enter BPM:")
    input()


def option5():
    cls()
    print("Enter pitch shift in semitones")
    input()


def option6():
    cls()
    print("Select background noise type:")
    input()


def option7():
    cls()
    print("Enter external WAV path to mix:")
    input()


def option8():
    cls()
    print("Rendering and playing...")
    input()


def option9():
    cls()
    print("Enter output WAV path:")
    input()


def option10():
    cls()
    yesNo = input("Are you sure you want to exit the program?(y=yes/n=no)")
    if yesNo == 'y':
        sys.exit()


if __name__ == "__main__":
    while (TRUE):
        cls()
        print("1) Selecting a waveform")
        print("2) Setting the loudness")
        print("3) Indicating the ABC file path")
        print("4) Changing speed (BPM)")
        print("5) Shifting pitch (semitones)")
        print("6) Adding background noise")
        print("7) Mixing within an external WAV file")
        print("8) Playing the file")
        print("9) Saving the music as a WAV file")
        print("10) exit")
        inputText = input("Please select a number between 1 and 10: ")
        match inputText:
            case '1':
                option1()
            case '2':
                option2()
            case '3':
                option3()
            case '4':
                option4()
            case '5':
                option5()
            case '6':
                option6()
            case '7':
                option7()
            case '8':
                option8()
            case '9':
                option9()
            case '10':
                option10()
            case _:
                cls()
                print("The input value is not valid. Please try again.")
                input()
