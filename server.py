# Echo server program
import socket, os
import controller.Controller as Controller

directionalControl = Controller()

directionSwitch = {
    104: directionalControl.go_backwards,
    100: directionalControl.go_left,
    102: directionalControl.go_right,
    98: directionalControl.go_forward
}

sock_name = '/tmp/uv4l.socket'              # Arbitrary non-privileged port
s = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
try:
    os.remove(sock_name)
except OSError:
    pass

s.bind(sock_name)
s.listen(1)

while 1:
    conn, addr = s.accept()

    while 1:
        data = conn.recv(1024)
        if not data: break
        directionSwitch[data]()
        conn.sendall(data)
    conn.close()
