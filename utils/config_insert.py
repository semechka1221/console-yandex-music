from utils import save_data

def setup_run() -> dict:
    print("Конфигурация данных.")
    client_data = {}

    while True:
        client_id = input("Введите Application ID (Нажмите ENTER для пропуска): ").strip()
        if client_id.isdigit():
            client_data["client_id"] = int(client_id)
            client_data["is_discord"] = True
            print("Для подключения изображения создайте ассет на Discord Developer Portal и назовите его 'avatar'.")
            break

        if not client_id:
            client_data["client_id"] = None
            client_data["is_discord"] = False
            break
        print("Ошибка: Application ID должен состоять исключительно из цифр.")

    yandex_token = input("Введите токен Яндекс Музыки: ").strip()
    client_data["token"] = yandex_token

    return client_data