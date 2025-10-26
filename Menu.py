# Menu for user interactions (provided by lecturer)
#sample.abc reference: https://abcnotation.com/examples
#
import os
from pickle import TRUE
import sys
import renderer

settings = {
    "waveform": "sine",
    "loudness": 0.5,
    "abcPath": "",
    "bpm": 120,
    "pitchShift": 0,
    "noiseType": None,
    "mixWavPath": None,
}


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def option1():
    cls()
    print("Select waveform:")
    settings["waveform"] = input().strip()


def option2():
    cls()
    print("Enter loudness:")
    try:
        settings["loudness"] = float(input().strip())
    except:
        print("Invalid loudness value.")
        input()


def option3():
    cls()
    print("Enter ABC file path:")
    i = input()
    settings["abcPath"] = i
    try:
        renderer.loadABC(i)
    except Exception as e:
        print("failed to load ABC:", e)
        input()


def option4():
    cls()
    print("Enter BPM:")
    settings["bpm"] = int(input().strip())


def option5():
    cls()
    print("Enter pitch shift in semitones")
    settings["pitchShift"] = int(input().strip())


def option6():
    cls()
    print("Select background noise type:")
    settings["noiseType"] = input().strip()


def option7():
    cls()
    print("Enter external WAV path to mix:")
    settings["mixWavPath"] = input().strip()


def option8():
    cls()
    print("Rendering and playing...")
    try:
        wave = renderer.renderMusic(
            waveform=settings["waveform"],
            volume=settings["loudness"],
            bpm=settings["bpm"],
            pitchShift=settings["pitchShift"]
        )
        renderer.play(wave)
    except Exception as e:
        print("Error during rendering or playback:", e)
        input()


def option9():
    cls()
    print("Enter output WAV path:")
    outPath = input().strip()
    wave = renderer.renderMusic(
        waveform=settings["waveform"],
        volume=settings["loudness"],
        bpm=settings["bpm"],
        pitchShift=settings["pitchShift"]
    )
    renderer.saveToWav(wave, outPath)
    print("Saved to", outPath)


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
