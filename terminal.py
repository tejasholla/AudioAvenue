from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
import subprocess, sys, os
import platform
import shlex

# You can add more words for auto-completion
linux_commands = ['echo', 'ls', 'cat', 'grep', 'find', 'exit']
command_completer = WordCompleter(linux_commands, ignore_case=True)

def execute_command(command):
    if platform.system() == "Windows":
        # Replace 'ls' with 'dir' on Windows
        command = command.replace('ls', 'dir')

    try:
        result = subprocess.run(shlex.split(command), shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}", file=sys.stderr)

def main():
    session = PromptSession(history=InMemoryHistory(), auto_suggest=AutoSuggestFromHistory(), completer=command_completer)

    while True:
        try:
            command = session.prompt("(MyTerminal) ", complete_while_typing=True)
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