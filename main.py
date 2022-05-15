from requests.exceptions import JSONDecodeError
from sys import argv
from absolute import abpath
from connection import Client, Downloader

VERSION = 1
HOST = "https://werryxgames.ml/pri/"

client = Client(HOST + "pri_server.php", VERSION)


def request_command():
    if len(argv) > 1:
        if argv[1] == "install":
            down = Downloader(client)
            for i in argv[2:]:
                if ".." in i:
                    print(f"Не удалось скачать '{i}'")
                else:
                    status = down.download(HOST + "files/" + i, abpath(i.split("/")[-1]))
                    if status == 0:
                        print(f"Файл '{i}' скачан успешно")
                    elif status == 1:
                        print(f"Файл '{i}' не найден")
                    elif status == 2:
                        print(f"Не удалось сохранить файл '{i}'")
    else:
        print("Python Remote Install")
        print(f"Версия: {VERSION}")


def main():
    try:
        response = client.send({"command": "test_connection"})
        data = response.json()
        if data["success"]:
            request_command()
        else:
            print(data["description"])
    except JSONDecodeError:
        print("Неверный ответ сервера")


if __name__ == '__main__':
    main()
