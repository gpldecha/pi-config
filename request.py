import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.1.105:5000")

socket.send_string("reset")
message = socket.recv_string()
print(message)
print('done')

