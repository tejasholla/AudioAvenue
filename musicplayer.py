import os
import pygame
import questionary
from questionary import Style


def initialize_music_player():
    pygame.mixer.init()

# Function to list all music files
def list_music_files(path):
    return [f for f in os.listdir(path) if f.endswith('.mp3')]

# Music control functions
def play_music(track):
    try:
        pygame.mixer.music.load(track)
        pygame.mixer.music.play()
    except pygame.error as e:
        print(f"Error playing {track}: {e}")

def pause_music():
    pygame.mixer.music.pause()

def resume_music():
    pygame.mixer.music.unpause()

def stop_music():
    pygame.mixer.music.stop()

def music_player_main(music_path):
    custom_style = Style([
        ('pointer', 'fg:red bold'),  # Color for the pointer
        ('highlighted', 'fg:red bold'),  # Color for highlighted item
        ('selected', 'fg:orange bg:#673ab7'),  # Color for selected item
    ])
    
    # Function to clear the screen
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    # Function to print the currently playing song with color
    def print_currently_playing(song):
        # ANSI escape code for color
        print(f"\033[94m\nCurrently Playing: {song}\033[0m")

    # Interactive Menu Options
    def menu_options(current_song):
        clear_screen()
        print_currently_playing(current_song)
        return questionary.select(
            "Please enter your choice:",
            choices=['Choose Song', 'Play/Pause', 'Resume', 'Stop', 'Next Track', 'Previous Track', 'Exit'],
            style=custom_style
        ).ask()

    # Function to choose a song or go back
    def choose_song(tracks, current_track_index):
        clear_screen()
        options = ["[Back to Main Menu]"] + tracks
        selected = questionary.select(
            "Select a song to play or go back:",
            choices=options,
            style=custom_style,
            pointer='->',
            default=options[current_track_index + 1]
        ).ask()
        return selected, options.index(selected) - 1
    
    tracks = list_music_files(music_path)

    if not tracks:
        print("No music files found in the provided path.")
        return

    current_track_index = 0
    play_music(os.path.join(music_path, tracks[current_track_index]))

    while True:
        choice = menu_options(tracks[current_track_index])

        if choice == 'Choose Song':
            selected_song, index = choose_song(tracks, current_track_index)
            if selected_song != "[Back to Main Menu]":
                current_track_index = index
                play_music(os.path.join(music_path, selected_song))
        elif choice == 'Play/Pause':
            if pygame.mixer.music.get_busy():
                pause_music()
            else:
                play_music(os.path.join(music_path, tracks[current_track_index]))
        elif choice == 'Resume':
            resume_music()
        elif choice == 'Stop':
            stop_music()
        elif choice == 'Next Track':
            current_track_index = (current_track_index + 1) % len(tracks)
            play_music(os.path.join(music_path, tracks[current_track_index]))
        elif choice == 'Previous Track':
            current_track_index = (current_track_index - 1) % len(tracks)
            play_music(os.path.join(music_path, tracks[current_track_index]))
        elif choice == 'Exit':
            break

    pygame.mixer.quit()

if __name__ == "__main__":
    music_path = "D:\Media\Music"
    initialize_music_player()
    music_player_main(music_path)

