from utils import setup_run
from utils import save_data

if __name__ == "__main__":

    data = setup_run()

    save_data('client', data)

    print("Конфигурация успешно сохранена!")