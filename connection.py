from requests import post, get
from threading import Thread


class Client:
    def __init__(self, host, version):
        self.main_host = host
        self.version = version

    def send(self, data, **kwargs):
        response = post(self.main_host, data={"type": "pri_request", "version": self.version, **data}, **kwargs)
        return response

    @staticmethod
    def raw_get(host, data=None, **kwargs):
        response = get(host, data=data, **kwargs)
        return response

    def get(self, data, **kwargs):
        response = self.raw_get(self.main_host, {"type": "pri_request", "version": self.version, **data}, **kwargs)
        return response


class Downloader:
    def __init__(self, client):
        self.client = client

    def download(self, path, output_file):
        response = self.client.raw_get(path)

        if response.status_code != 200:
            return 1

        try:
            with open(output_file, "wb") as f:
                f.write(response.content)
        except (FileNotFoundError, OSError, PermissionError):
            return 2

        return 0

    def async_download(self, *args):
        thr = Thread(target=self.download, args=(*args,))
        thr.start()

        return thr
