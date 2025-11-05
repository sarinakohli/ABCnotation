# Menu for user interactions (base provided by lecturer)
# sample.abc reference: https://abcnotation.com/examples

# relevant imports
import os
from pickle import TRUE
import sys
import renderer

# default settings used in menu options
settings = {
    "waveform": "sine",
    "loudness": 0.5,
    "abcPath": "",
    "bpm": 120,
    "pitchShift": 0,
    "noiseType": None,
    "mixWavPath": None,
}

# clear screen function


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

# menu option functions
# selecting waveform


def option1():
    cls()
    print("Select waveform:")
    settings["waveform"] = input().strip()

# setting loudness


def option2():
    cls()
    print("Enter loudness:")
    try:
        settings["loudness"] = float(input().strip())
    except:
        print("Invalid loudness value.")
        input()

# renderer load ABC file from renderer module


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

# changing BPM


def option4():
    cls()
    print("Enter BPM:")
    try:
        settings["bpm"] = int(input().strip())
        print("BPM updated to:", settings["bpm"])
    except ValueError:
        print("Invalid BPM value. Please enter a valid integer.")
        input("Press Enter to continue...")

# shifting pitch


def option5():
    cls()
    print("Enter pitch shift in semitones")
    settings["pitchShift"] = int(input().strip())

# adding background noise


def option6():
    cls()
    print("Select background noise type:")
    i = input().strip().lower()
    if i in ["white", "pink", "brown"]:
        settings["noiseType"] = i
        print("Noise type set to:", {i})
    else:
        settings["noiseType"] = None
        print("Invalid noise type. No noise will be added.")
    input("Press Enter to continue...")

# mixing within an external WAV file


def option7():
    cls()
    print("Enter external WAV path to mix:")
    i = input()
    settings["mixWavPath"] = i
    print("External WAV file set to:", {i})
    input("Press Enter to continue...")

# renders and plays music using renderer module for both .abc and .wav mixing


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

        if settings.get("mixWavPath"):
            wave = renderer.mixWithWav(wave, settings["mixWavPath"])

        if settings.get("noiseType"):
            wave = renderer.add_noise(wave, settings["noiseType"])

        renderer.play(wave)
    except Exception as e:
        print("Error during rendering or playback:", e)
        input()

# saves rendered music to WAV file (mixing and non-mixing)


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

    if settings.get("mixWavPath"):
        wave = renderer.mixWithWav(wave, settings["mixWavPath"])

    if settings.get("noiseType"):
        wave = renderer.add_noise(wave, settings["noiseType"])

    renderer.saveToWav(wave, outPath)
    print("Saved to", outPath)

# saves rendered music to MIDI file


def option10():
    cls()
    if not settings["abcPath"]:
        print("No ABC file loaded.")
        input("Press Enter to continue...")
        return
    print("Enter output MIDI file path:")
    outPath = input().strip()
    renderer.saveToMidi(settings["abcPath"], outPath)
    input("Press Enter to continue...")


# exit program


def option11():
    cls()
    yesNo = input("Are you sure you want to exit the program?(y=yes/n=no)")
    if yesNo == 'y':
        sys.exit()


# main loop
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
        print("10) Saving the music as a MIDI file")
        print("11) exit")
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
            case '11':
                option10()
            case _:
                cls()
                print("The input value is not valid. Please try again.")
                input()
