from pypresence import ActivityType, Presence
from utils import load_data
import time

def start_discord_activity(track_name: str, artists: str, track_len: float) -> None:

    CLIENT = load_data("client")

    rpc = Presence(str(CLIENT["client_id"]))
    rpc.connect()

    rpc.update(
        state=artists,
        name='YandexConsole Player',
        details=track_name,
        activity_type=ActivityType.LISTENING,
        start=int(time.time()),
        end=int(time.time())+track_len,
        large_image="avatar"      
    )

def start_neutral_discord_activity() -> None:

    CLIENT = load_data("client")

    rpc = Presence(str(CLIENT["client_id"]))
    rpc.connect()

    rpc.update(
        activity_type=ActivityType.LISTENING,
        name="YandexConsole Player",
        details="Выбирает трек",
        large_image="avatar"
    )