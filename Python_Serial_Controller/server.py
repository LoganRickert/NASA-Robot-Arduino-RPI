import socket
from time import sleep
from threading import Lock
from threading import Thread
import RaspberryPi

class Server:
    
    def __init__(self, addr, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = addr
        self.port = port
        self.server_addr = (addr, port)

    def setup_server(self):
        self._socket.bind(self.server_addr)
        self._socket.listen(5)

    def begin(self):
        while True:
            print 'Waiting for clients on', self.server_addr
            client, addr = self._socket.accept()

            data = self.recvall(client)

            if data == 'raspberrypi':
                print "Raspberry Pi connected."
                client.send('okay\n')
                thread = Thread(target=self.update_raspberrypi, args=(client,))
                thread.start()
            elif data == 'gui':
                print "GUI connected."
                client.send('okay')
                thread = Thread(target=self.update_gui, args=(client,))
                thread.start()
            else:
                print 'None of the above.', list(data)
                client.close()

    def update_raspberrypi(self, client):
        raspberrypi = RaspberryPi.RaspberryPi()

        while True:
            sleep(0.5) # Sleep 500 milliseconds
            raspberrypi.update(client)
            client.send('Updated.')


    def update_gui(self, client):
        pass

    def recvall(self, socket):
        data = "z"

        print "Recvalling."

        while data[-1] != "\n":
            packet = socket.recv(1024)
            print list(packet)
            data += packet

        return ''.join(data[1:].split())


if __name__ == "__main__":
    print "starting script"
    server = Server('', 1336)
    server.setup_server()
    server.begin()
