############## IMPORTS ##############
import os
import re
import sys
import mutagen
from mutagen.mp3 import MP3
from mutagen.flac import FLAC

############# VARIABLES #############
red      = "\033[1;31m"
green    = "\033[1;32m"
yellow   = "\033[1;33m"
no_color = "\033[0m"

############# FUNCTIONS #############
def lowercase_match(match):
    """Lowercase the whole regular expression match group."""
    return match.group().lower()

def title(value):
    titled = value.title()
    titled = re.sub(r"([a-z])'([A-Z])", lowercase_match, titled)  # Fix Don'T
    titled = re.sub(r"\d([A-Z])", lowercase_match, titled)  # Fix 1St and 2Nd
    return titled

def prettify(str):
    str = str.strip()
    str = title(str)
    return str 

def rename(path, current_name, new_name):
    current_file = path + "\\" + current_name
    new_file     = path + "\\" + new_name

    print(f"Renaming '{yellow}{current_name}{no_color}' to '{yellow}{new_name}{no_color}'...")
    os.rename(current_file, new_file)

def handle_mp3(path, track, file):
    # Artist
    if ("TPE1" in track.keys()):
        artist = str(track.get("TPE1"))
        artist = prettify(artist)

    # Track Title
    if ("TIT2" in track.keys()):
        title = str(track.get("TIT2"))
        title = prettify(title)

    if artist and title:
        new_name = artist + " - " + title + ".mp3"
        rename(path, file, new_name)

def main(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = folder_path + "\\" + file_name

        if os.path.isdir(file_path):
            # Recursive Call
            main(file_path)
        elif os.path.isfile(file_path):
            file      = mutagen.File(file_path)
            file_type = type(file)

            if file_type == mutagen.mp3.MP3:
                track = MP3(file_path)
                handle_mp3(folder_path, track, file_name)
            elif file_type == mutagen.flac.FLAC:
                file = FLAC(file_path)
            else:
                print(f"{yellow}File type {type} not supported...{no_color}")

def exit_program():
    print(f"{green}BYE!!{no_color}")
    sys.exit(0)

############### CODE ################
# folder = "C:\\Users\\Christos\\Desktop\\Rename_TEST\\"

print("#######################################################################################")
while True:
    ui = input(f"Enter the {green}file path{no_color} that contains the files to be renamed or enter {red}n{no_color} to exit: ")

    if ui != "n" and not os.path.isdir(ui):
        print("Please enter a correct file path: ")
        continue
    else:
        break

if ui == "n":
    exit_program()
else:
    folder = ui

while True:
    print(f"The directory is set to {yellow}'{folder}'{no_color}.")
    ui = input(f"Are you sure you want to rename all the music files inside this directory? ({green}y{no_color}/{red}n{no_color}) ")

    if ui == "y" or ui == "n":
        break
    else:
        print(f"Please answer {green}y{no_color} or {red}n{no_color}")
        continue
print("#######################################################################################")

if ui == "n":
    exit_program()
else:
    main(folder)