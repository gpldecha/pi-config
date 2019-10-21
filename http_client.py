import urllib.error
from urllib.request import urlopen
import cv2
import numpy as np
import time
import threading
import queue
import signal


class HttpClient(threading.Thread):

    def __init__(self, url, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self._url = url
        self._stopper = threading.Event()
        self._image_lifo_queue = queue.LifoQueue(maxsize=2)
        self.daemon = True

    def get_image(self):
        if self._image_lifo_queue.empty():
            return None
        else:
            return self._image_lifo_queue.get()

    def stopit(self):
        self._stopper.set()

    def stopped(self):
        return self._stopper.isSet()

    def run(self):
        stream = urlopen(self._url)
        bytes_ = b''
        a = -1
        b = -1
        t = time.time()
        while not self.stopped():
            try:
                data = stream.read(4096)
            except KeyboardInterrupt as e:
                stream.close()
                self.stopit()
                continue

            if len(data) == 0:
                if time.time() - t > 2:
                    try:
                        stream = urlopen(self._url)
                    except urllib.error.URLError as e:
                        print("No connection")
                    bytes_ = b''
                    t = time.time()

            bytes_ += data
            if a == -1:
                a = bytes_.find(b'\xff\xd8')
            if b == -1:
                b = bytes_.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes_[a:b + 2]
                bytes_ = bytes_[b + 2:]
                a = -1
                b = -1
                image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                if self._image_lifo_queue.full():
                    self._image_lifo_queue.get()
                try:
                    self._image_lifo_queue.put(np.copy(image))
                except:
                    print('Unable to put')
        stream.close()
        print('Exiting HttpClient thread')


class Visualise:

    def __init__(self):
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)

    def update(self, image):
        if image is None: return
        try:
            cv2.imshow('image', image)
            cv2.waitKey(1)
        except:
            pass


def signal_handler(sig, frame, flag, stop):
    flag[0] = True
    stop()
    print('You pressed Ctrl+C!')
    exit()


if __name__ == "__main__":

    # http_client = HttpClient("http://192.168.1.105:8080")
    http_client = HttpClient("http://192.168.2.2:8080")
    http_client.start()
    flagg = [False]
    signal.signal(signal.SIGINT,
                  lambda sig, frame: signal_handler(sig, frame, flagg, http_client.stopit))

    visualise = Visualise()

    while not flagg[0]:
        image = http_client.get_image()
        visualise.update(image)

    print('Exiting')
