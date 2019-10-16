import urllib
import cv2
import numpy as np
import time

stream = urllib.urlopen("http://192.168.1.105:8080")
bytes=''
a = -1
b = -1
t = time.time()
c = 0
while True:

    bytes += stream.read(4096)
    if a == -1:
        a = bytes.find('\xff\xd8')
    if b == -1:
        b = bytes.find('\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b + 2]
        bytes = bytes[b + 2:]
        a = -1
        b = -1
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('i', i)
        c += 1
        if cv2.waitKey(1) == 27:
            exit(0)
    if time.time() - t >= 1.0:
        print(c)
        c = 0
        t = time.time()
