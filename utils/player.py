from yandex_music import Client
import tempfile
import pygame
import os
from utils import load_data
from utils import start_discord_activity, start_neutral_discord_activity

class YandexMusicPlayer:

    def __init__(self, token):
        self.client = Client(token).init()
        self.is_discord = load_data('client')["is_discord"]

        self.is_playing: bool = False
        self.is_paused: bool = False
        self.is_playlist: bool = False

        self.current_track_path = None
        self.track = None

        self.duration: float = 0.0

        self.is_playlist_stopping: bool = False

    def play_track(self, track_name: str) -> None:

        try:
            search_result = self.client.search(track_name)

            if not search_result or not search_result.tracks or len(search_result.tracks.results) == 0:
                print("⚠️・Трек не найден!")
                return

            track = search_result.tracks.results[0]
            self.track = track

            artists = ", ".join(artist.name for artist in track.artists)
            print(f"▶️・Играет: {track.title} - {artists}")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_path = temp_file.name

            track.download(temp_path)
            self.current_track_path = temp_path

            pygame.mixer.music.load(self.current_track_path)
            pygame.mixer.music.play()

            try:
                if hasattr(track, "duration") and track.duration is not None:
                    self.duration = track.duration / 1000.0
                else:
                    sound = pygame.mixer.Sound(self.current_track_path)
                    self.duration = sound.get_length()
            except Exception:
                self.duration = 0.0

            self.is_playing = True
            self.is_paused = False

            if self.is_discord:
                start_discord_activity(track.title, artists, self.duration)

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.is_playing = False
            self.is_paused = False

    def pause(self) -> None:

        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            print("⏸️・Пауза")

    def unpause(self) -> None:

        if self.is_paused and self.is_playing:
            pygame.mixer.music.unpause()
            self.is_paused = False
            print("▶️・Продолжено")

    def stop(self) -> None:

        if self.is_playing or self.is_paused:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            if self.is_discord: start_neutral_discord_activity()
            print("⏹️・Остановлено")

        self.is_playing = False
        self.is_paused = False

        if self.current_track_path and os.path.exists(self.current_track_path):
            try:
                os.remove(self.current_track_path)
            except OSError as e:
                print(f"⚠️・Не удалось удалить временный файл: {e}")
            finally:
                self.current_track_path = None