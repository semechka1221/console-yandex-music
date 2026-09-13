from utils import YandexMusicPlayer
from utils import Playlists
from utils import restart_console
from utils import start_neutral_discord_activity
import pygame

def handler(player: YandexMusicPlayer, playlist: Playlists, music_end) -> None:
    while True:

        for event in pygame.event.get():

            if event.type == music_end:
                if player.is_playlist:
                    restart_console("playlist", playlist)
                    playlist.next(True)

                else:
                    restart_console()
                    if player.is_discord: start_neutral_discord_activity()
                    print("⏹️・Проигрывание завершено.")
                    print("Введите команду: ", end="")
