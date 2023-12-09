import os
import pygame
import questionary
from questionary import Style
import time
from mutagen.mp3 import MP3
import threading

progress_thread_running = False

def initialize_music_player():
    pygame.mixer.init()

# Function to list all music files
def list_music_files(path):
    return [f for f in os.listdir(path) if f.endswith('.mp3')]

def search_songs(tracks, query):
    """
    Search for songs in tracks list that contain the query string.
    """
    query = query.lower()
    return [track for track in tracks if query in track.lower()]

# Crossfade function
def crossfade_tracks(old_track, new_track, duration=2):
    """
    Crossfade from old_track to new_track over the specified duration (in seconds).
    """
    max_volume = pygame.mixer.music.get_volume()
    step = max_volume / (duration * 10)  # Calculate volume change per step

    # Fade out the old track
    for _ in range(int(duration * 10)):
        current_volume = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(max(0, current_volume - step))
        time.sleep(0.1)

    # Stop the old track and start the new one
    pygame.mixer.music.stop()
    pygame.mixer.music.load(new_track)
    pygame.mixer.music.play()

    # Fade in the new track
    for _ in range(int(duration * 10)):
        current_volume = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(min(max_volume, current_volume + step))
        time.sleep(0.1)

def get_song_duration(file_path):
    """
    Get the duration of a song.
    """
    audio = MP3(file_path)
    return audio.info.length

def display_progress(current_song):
    global progress_thread_running
    duration = get_song_duration(current_song)
    while pygame.mixer.music.get_busy() and progress_thread_running:
        position = pygame.mixer.music.get_pos() / 1000.0  # Convert to seconds
        print(f"\rCurrent Progress: {format_time(position)} / {format_time(duration)}", end='')
        time.sleep(1)

def format_time(seconds):
    """
    Format time in seconds to a string in the format 'minutes:seconds'.
    """
    return f"{int(seconds // 60)}:{int(seconds % 60):02d}"

# Music control functions
def play_music(new_track):
    global progress_thread_running
    progress_thread_running = True  # Set the flag to True when starting playback
    try:
        current_track = pygame.mixer.music.get_pos()
        if current_track != -1:  # Check if a track is already playing
            crossfade_tracks(current_track, new_track)
        else:
            pygame.mixer.music.load(new_track)
            pygame.mixer.music.play()
            # Start a new thread to display the progress
            progress_thread = threading.Thread(target=display_progress, args=(new_track,))
            progress_thread.start()
    except pygame.error as e:
        print(f"Error playing {new_track}: {e}")

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

    def search_and_choose_song(tracks):
        """
        Search for songs based on user input and allow the user to choose a song from the search results.
        """
        while True:
            query = questionary.text("Enter song name to search:").ask()
        
            search_results = search_songs(tracks, query)

            if not search_results:
                print("No songs found. Try again.")
                continue

            choices = search_results + ['Search again', 'Back to Main Menu']
            selected = questionary.select(
                "Select a song to play, search again, or go back:",
                choices=choices,
                style=custom_style,
                pointer='->'
            ).ask()

            if selected == 'Back to Main Menu':
                return None, -1
            elif selected == 'Search again':
                continue
            else:
                return selected, tracks.index(selected)
        
    # Function to choose a song or go back
    def choose_song(tracks, current_track_index):
        clear_screen()
        action = questionary.select(
            "Do you want to search for a song or choose from the list?",
            choices=['Search for a song', 'Choose from the list'],
            style=custom_style
        ).ask()

        if action == 'Search for a song':
            selected_song, index = search_and_choose_song(tracks)
            if selected_song is None:
                # User chose 'Go Back', return to previous menu without action
                return None, current_track_index
            else:
                return selected_song, index
        else:
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
            if selected_song and selected_song != "[Back to Main Menu]":
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

    progress_thread_running = False
    pygame.mixer.quit()

if __name__ == "__main__":
    music_path = "D:\Media\Music"
    initialize_music_player()
    music_player_main(music_path)

