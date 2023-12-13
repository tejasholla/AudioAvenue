import tkinter as tk
import subprocess
import threading
import queue

# Define process as a global variable
global process

def enqueue_output(out, queue):
    """Enqueue each line of output from the subprocess."""
    for line in iter(out.readline, ''):
        queue.put(line)
    out.close()

def run_script():
    """Run the Python script and capture its output."""
    global process
    process = subprocess.Popen(["python", "ytDownloader.py"], 
                               stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, 
                               text=True, 
                               bufsize=1)

    # Thread for handling script output
    q = queue.Queue()
    output_thread = threading.Thread(target=enqueue_output, args=(process.stdout, q))
    output_thread.daemon = True
    output_thread.start()

    # Continuously update output to the text widget
    def update_output():
        try:
            line = q.get_nowait()
        except queue.Empty:
            pass
        else:
            text_widget.insert(tk.END, line)
            text_widget.see(tk.END)
        root.after(100, update_output)

    update_output()

def on_key(event):
    """Send key press events to the subprocess."""
    global process
    try:
        process.stdin.write(event.char)
        process.stdin.flush()
    except Exception as e:
        print("Error sending input:", e)

# Create the main window
root = tk.Tk()
root.title("Python Script Terminal")

# Create a text widget for output
text_widget = tk.Text(root)
text_widget.pack(expand=True, fill=tk.BOTH)

# Bind key events to the handler
root.bind('<Key>', on_key)

# Run the script in a separate thread to avoid freezing the GUI
thread = threading.Thread(target=run_script, daemon=True)
thread.start()

# Start the Tkinter event loop
root.mainloop()
