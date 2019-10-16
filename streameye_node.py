import zmq
import argparse
import time
import subprocess


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Streameye node.')
    parser.add_argument('--port', type=str, default='5000', help='port to listen on')
    args = parser.parse_args()

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://0.0.0.0:" + args.port)

    print('start streaming')
    cmd = 'python3 raspimjpeg.py -w 640 -h 480 -q 5 --vflip --awb=off -r 60 | streameye'
    proc = subprocess.Popen(cmd, shell=True)

    while True:

        message = socket.recv_pyobj()
        print('stopping camera')
        proc.terminate()
        time.sleep(3)
        print('start streaming')
        proc = subprocess.Popen(cmd, shell=True)
        socket.send("Ok")

