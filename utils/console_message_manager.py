import subprocess
import os
from utils import Playlists

def clear_console() -> None:

    if os.name == 'nt':
        subprocess.run(['cmd', '/c', 'cls'], check=False)
    else:
        subprocess.run(['clear'], check=False)

def restart_console(mode: str = "base", playlist: Playlists = None) -> None:

    message_base = """
    Привет!
    Список команд:
    1. new, play "название трека"
    2. pause
    3. resume
    4. stop
    5. playlists
    6. exit
    """

    message_playlist = f"""
    Режим плейлистов.
    Текущий плейлист: {playlist.current_playlist_name.replace(".json", "") if playlist and playlist.current_playlist_name else "Не выбран"}
    Список команд:
    1. list
    2. play "название плейлиста"
    3. add "название трека"
    4. new "название плейлиста"
    5. select "название плейлиста"
    6. stop
    7. leave
    """

    if mode == "base":

        clear_console()
        
        print(message_base)

    if mode == "playlist":

        clear_console()

        print(message_playlist)