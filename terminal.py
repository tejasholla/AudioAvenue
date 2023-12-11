from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
import subprocess, sys, os
import platform
import shlex

# Adding 'downloadyt' to the list of commands
linux_commands = ['echo', 'ls', 'cat', 'grep', 'find', 'exit', 'downloadyt']
command_completer = WordCompleter(linux_commands, ignore_case=True)

def execute_ytDownloader():
    # Directly executing ytDownloader.py
    os.system('python ytDownloader.py')

def execute_command(command):
    if platform.system() == "Windows":
        command = command.replace('ls', 'dir')

    # Check if the command is 'downloadyt'
    if command.strip().lower() == 'downloadyt':
        execute_ytDownloader()
        return

    try:
        result = subprocess.run(shlex.split(command), shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}", file=sys.stderr)

def main():
    session = PromptSession(history=InMemoryHistory(), auto_suggest=AutoSuggestFromHistory(), completer=command_completer)

    while True:
        try:
            command = session.prompt("(Ghost-Terminal) ", complete_while_typing=True)
            if command.strip().lower() == 'exit':
                break
            execute_command(command)
        except KeyboardInterrupt:
            continue  # Ctrl-C pressed. Try again.
        except EOFError:
            break  # Ctrl-D pressed.

    print('Goodbye!')

if __name__ == '__main__':
    main()
