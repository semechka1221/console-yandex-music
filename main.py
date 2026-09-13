from utils import YandexMusicPlayer
from utils import Playlists
from utils import load_data
from utils import restart_console
from utils import start_neutral_discord_activity
from utils import handler
import pygame
import threading
import time

if __name__ == "__main__":
    MUSIC_END = pygame.USEREVENT+1
    pygame.mixer.music.set_endevent(MUSIC_END)
    pygame.init()
    pygame.mixer.init()

    CLIENT = load_data("client")

    player = YandexMusicPlayer(CLIENT["token"])
    playlist = Playlists(player)
    current_mode: str = "player"

    if CLIENT['is_discord']: start_neutral_discord_activity()

    event_listener = threading.Thread(target=handler, args=(player, playlist, MUSIC_END))
    event_listener.start()

    restart_console()

    while True:
        time.sleep(0.5)
        command = input("Введите команду: ").strip()

        if current_mode == "player":

            restart_mode = "base"

            if "playlists" in command:
                command = command.replace("playlists", "")
                restart_console("playlist")
                player.is_playlist = True
                player.stop()
                current_mode = "playlists"

            elif "play" in command:
                command = command.replace("play ", "")
                restart_console(restart_mode)
                player.play_track(command)

            elif "unpause" in command or "resume" in command:
                command = command.replace("unpause", "").replace("resume", "")
                restart_console(restart_mode)
                player.unpause()

            elif "pause" in command:
                command = command.replace("pause", "")
                restart_console(restart_mode)
                player.pause()

            elif "stop" in command:
                command = command.replace("stop", "")
                restart_console(restart_mode)
                player.stop()

            elif "exit" in command:
                command = command.replace("exit", "")
                player.stop()
                raise SystemExit()

        elif current_mode == "playlists":

            restart_mode = "playlist"

            if "play" in command:
                command = command.replace("play ", "")
                restart_console(restart_mode, playlist)
                playlist.play(command)

            elif "new" in command:
                command = command.replace("new ", "")
                restart_console(restart_mode, playlist)
                playlist.create(command)

            elif "list" in command:
                command = command.replace("list", "")
                restart_console(restart_mode, playlist)
                playlist.get_list()

            elif "add" in command:
                command = command.replace("add ", "")
                restart_console(restart_mode, playlist)
                playlist.add_track(command)

            elif "select" in command:
                command = command.replace("select ", "")
                restart_console(restart_mode, playlist)
                playlist.select(command)

            elif "stop" in command:
                command = command.replace("stop", "")
                restart_console(restart_mode, playlist)
                player.stop()

            elif "leave" in command:
                command = command.replace("stop", "")
                player.stop()
                restart_console("base")
                current_mode = "player"
                player.is_playlist = False
