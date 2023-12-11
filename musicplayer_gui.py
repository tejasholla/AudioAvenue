import os
import pygame
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from mutagen.mp3 import MP3

class MusicPlayerGUI:
    def __init__(self, root):
        self.root = root
        root.title("Music Player")
        root.configure(bg='#2c2c2c')  # Set the background color to dark gray
        root.geometry("800x600")

        standard_font = ("Arial", 10)
        # Set the transparency of the window
        root.attributes('-alpha', 0.95)  # Adjust the value as needed, e.g., 0.95 for 95% opacity

        # Initialize Pygame mixer
        pygame.mixer.init()

        # Variables
        self.track_list = []
        self.current_track_index = 0
        self.music_folder = "D:\\Media\\Music"
        self.is_playing = False
        self.is_paused = False

        # Left Frame for Songs List and Load Button
        self.left_frame = tk.Frame(root, bg='#2c2c2c')
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Load Button
        self.load_button = tk.Button(self.left_frame, text='Load Music Folder', command=self.load_music_folder, bg='#ff8c00', fg='black')
        self.load_button.pack(fill=tk.X)

        # Songs Listbox
        self.track_listbox = tk.Listbox(self.left_frame, bg='#2c2c2c', fg='white', selectbackground='orange')
        self.track_listbox.pack(fill=tk.BOTH, expand=True)

        # Right Frame for Song Details
        self.right_frame = tk.Frame(root, bg='#2c2c2c')
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Song Image Placeholder
        self.song_image_label = tk.Label(self.right_frame, text='Song Image', bg='black', width=20, height=10)
        self.song_image_label.pack(anchor='center', pady=20)

        # Song Name Label
        self.song_name_label = tk.Label(self.right_frame, text='Song Name', bg='#2c2c2c', fg='white')
        self.song_name_label.pack()

        # Control Buttons Frame
        self.controls_frame = tk.Frame(self.right_frame, bg='#2c2c2c')
        self.controls_frame.pack(anchor='center', pady=20)

        # Progress Bar
        # self.progress = ttk.Progressbar(self.controls_frame, orient='horizontal', mode='determinate', length=100)
        # self.progress.pack(fill=tk.X)

        # Previous Button
        self.prev_button = tk.Button(self.controls_frame, text='Previous', command=self.prev_track, bg='#ff8c00', fg='black')
        self.prev_button.pack(side=tk.LEFT, padx=5)

        # Play/Pause Button
        self.play_pause_button = tk.Button(self.controls_frame, text='Play', command=self.toggle_play_pause, bg='#ff8c00', fg='black')
        self.play_pause_button.pack(side=tk.LEFT, padx=5)

        # Stop Button
        self.stop_button = tk.Button(self.controls_frame, text='Stop', command=self.stop_music, bg='#ff8c00', fg='black')
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Next Button
        self.next_button = tk.Button(self.controls_frame, text='Next', command=self.next_track, bg='#ff8c00', fg='black')
        self.next_button.pack(side=tk.LEFT, padx=5)

        # Center the control buttons
        self.controls_frame.pack(anchor='center')

        # Update the font for buttons and labels
        self.load_button.configure(font=standard_font)
        self.track_listbox.configure(font=standard_font)

        self.song_image_label.configure(font=standard_font)
        self.song_name_label.configure(font=standard_font)
        # self.song_details_label.configure(font=standard_font)  # Uncomment if you use it

        self.prev_button.configure(font=standard_font)
        self.play_pause_button.configure(font=standard_font)
        self.stop_button.configure(font=standard_font)
        self.next_button.configure(font=standard_font)

    def update_song_selection(self):
        # Clear previous selection
        for i in range(self.track_listbox.size()):
            self.track_listbox.itemconfig(i, {'bg': '#2c2c2c'})

        # Highlight the current track
        if self.current_track_index is not None:
            self.track_listbox.selection_clear(0, tk.END)
            self.track_listbox.selection_set(self.current_track_index)
            self.track_listbox.activate(self.current_track_index)
            self.track_listbox.itemconfig(self.current_track_index, {'fg': 'orange'})
            self.track_listbox.see(self.current_track_index)  # Ensure the current track is visible

    def load_music_folder(self):
        self.music_folder = filedialog.askdirectory()
        if self.music_folder:
            self.track_list = [f for f in os.listdir(self.music_folder) if f.endswith('.mp3')]
            self.track_listbox.delete(0, tk.END)
            for track in self.track_list:
                self.track_listbox.insert(tk.END, track)

    def toggle_play_pause(self):
        if not self.track_list:
            return

        if not self.is_playing or self.is_paused:
            self.resume_music()
        else:
            self.pause_music()

    def play_music(self, track_index=None):
        if track_index is not None:
            self.current_track_index = track_index
        else:
            selected_index = self.track_listbox.curselection()
            if selected_index:
                self.current_track_index = selected_index[0]

        track_name = self.track_list[self.current_track_index]
        track_path = os.path.abspath(os.path.join(self.music_folder, track_name))

        try:
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            self.play_pause_button.config(text='Pause')

            # Update the song name label with the current track's name
            self.song_name_label.config(text=track_name)
            # Update the selection in the listbox
            self.update_song_selection()

        except pygame.error as e:
            messagebox.showerror("Error playing track", f"An error occurred: {e}")

    def pause_music(self):
        pygame.mixer.music.pause()
        self.is_playing = False
        self.is_paused = True
        self.play_pause_button.config(text='Play')

    def resume_music(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
        else:
            self.play_music()
        self.is_playing = True
        self.play_pause_button.config(text='Pause')

    def stop_music(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.play_pause_button.config(text='Play')

    def next_track(self):
        if self.track_list:  # Check if the list is not empty
            self.current_track_index = (self.current_track_index + 1) % len(self.track_list)
            self.play_music(self.current_track_index)

    def prev_track(self):
        if self.track_list:  # Check if the list is not empty
            self.current_track_index = (self.current_track_index - 1) % len(self.track_list)
            self.play_music(self.current_track_index)

# Main
if __name__ == "__main__":
    root = tk.Tk()
    gui = MusicPlayerGUI(root)
    root.mainloop()
