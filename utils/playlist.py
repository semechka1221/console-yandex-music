from pathlib import Path
import json
from utils import YandexMusicPlayer

class Playlists:

    def __init__(self, player: YandexMusicPlayer):

        self.player = player

        self.base_dir = Path(__file__).resolve().parent.parent
        self.playlists_dir = self.base_dir / "playlists"

        self.playlists_dir.mkdir(parents=True, exist_ok=True)

        self.playlist_files: list = [
            f.name for f in self.playlists_dir.iterdir()
            if f.is_file() and f.suffix.lower() == ".json"
        ]

        self.current_playlist: list = None
        self.current_track_number: int = 0
        self.current_playlist_name: str = None

    def _get_playlist_path(self, name: str) -> Path:

        if not name.endswith(".json"):
            name = f'{name}.json'

        return self.playlists_dir / name

    def get_list(self) -> None:
        print("Список ваших плейлистов:")

        if not self.playlist_files:
            print("⚠️・У вас 0 плейлистов!")
            return

        for number, filename in enumerate(self.playlist_files):
            display_name = filename.replace(".json", "") if filename.lower().endswith(".json") else filename

            print(f'{number}. {display_name}')

    def play(self, name: str) -> None:

        filename = f'{name}.json' if not name.lower().endswith(".json") else name

        if filename not in self.playlist_files:
            print("⚠️・Данный плейлист не существует!")
            return

        path = self._get_playlist_path(filename)

        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)

        except Exception as e:
            print(f"⚠️・Ошибка: {e}")

        self.current_playlist = []

        for value in data.values():
            self.current_playlist.append({
                "title": str(value["title"]),
                "artist": str(value["artist"])
            })

        if not self.current_playlist:
            print("⚠️・Плейлист пуст!")

        self.current_playlist_name = filename
        self.current_track_number = 0
        self._play_current_track()

    def _play_current_track(self) -> None:

        track = self.current_playlist[self.current_track_number]
        track_str = f'{track['title']} - {track['artist']}'

        self.player.play_track(track_str)

    def next(self, start: bool = True) -> None:

        if not self.current_playlist:
            print("⚠️・Нет активного плейлиста!")
            return

        if start:
            self.current_track_number += 1

            if self.current_track_number >= len(self.current_playlist):
                self.current_track_number = 0

            self._play_current_track()

        else:
            self.player.stop()

    def create(self, name: str = "") -> None:

        if not name:
            print("⚠️・Введите название плейлиста!")
            return

        filename = f'{name}.json'if not name.lower().endswith(".json") else name
        path = self._get_playlist_path(filename)

        if path.exists():
            print("⚠️・Такой плейлист уже существует!")
            return

        starting = {}

        try:

            path.parent.mkdir(parents=True, exist_ok=True)

            with path.open("w", encoding="utf-8") as file:
                json.dump(starting, file, ensure_ascii=False, indent=4)

            self.playlist_files.append(filename)

            print(f"✅・Плейлист {name} успешно создан!")

        except Exception as e:
            print(f"⚠️・Не удалось создать плейлист!\nОшибка: {e}")

    def add_track(self, track_data: str) -> None:

        if not track_data or not self.current_playlist_name:
            print("⚠️・Введите название трека и выберите плейлист с помощью команды select!")
            return

        search = self.player.client.search(track_data)

        if not search or not search.tracks or len(search.tracks.results) == 0:
            print("⚠️・Трек не найден!")
            return

        track = search.tracks.results[0]
        artists = ", ".join(artist.name for artist in track.artists)

        path = self._get_playlist_path(self.current_playlist_name)

        try:
            with path.open("r", encoding="utf-8") as file:
                playlist_data = json.load(file)

        except Exception:
            playlist_data = {}

        new_index = str(len(playlist_data) + 1)
        playlist_data[new_index] = {
            "title": track.title,
            "artist": artists
        }

        try:
            with path.open("w", encoding="utf-8") as file:
                json.dump(playlist_data, file, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"⚠️・Не удалось сохранить плейлист!\nОшибка: {e}")
            return

        self.current_playlist.append({
            "title": track.title,
            "artist": artists
        })

        print(f"✅・Трек '{track.title} - {artists}' успешно добавлен в плейлист {self.current_playlist_name.replace(".json", "")}!")

    def select(self, name: str) -> None:

        if not name:
            print("⚠️・Введите название плейлиста!")
            return

        filename = f'{name}.json' if not name.lower().endswith(".json") else name

        if filename not in self.playlist_files:
            print("⚠️・Данный плейлист не существует!")
            return
        
        path = self._get_playlist_path(filename)
        
        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)

        except Exception as e:
            print(f"⚠️・Ошибка: {e}")
        
        self.current_playlist = []
        
        for value in data.values():
            self.current_playlist.append({
                "title": str(value["title"]),
                "artist": str(value["artist"])
            })

        self.current_playlist_name = filename

        print(f"✅・Успешно выбран плейлист: {self.current_playlist_name.replace(".json", "")}!")