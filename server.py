import socket
import threading

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, int(self.port)))

    def listen(self):
        clients=[];
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            #client.settimeout(60)
            clients.append(["name",0,Lock()])
            threading.Thread(target = self.listenToClient,args=  (clients[len(clients)-1],client,address)).start()

    def listenToClient(self, clientpair, client, address):
        size = 1024

        #name
        data = client.recv(size)
        clientpair[0]=data.rstrip()
        print(clientpair[0])

        #state
        data = client.recv(size)
        clientpair[1]=data.rstrip()
        print(clientpair[1])

        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data
                    response = data
                    client.send(response)
                else:
                    raise error('Client disconnected')
            except:
                #remove on close
                client.close()
                return False

if __name__ == "__main__":
    port_num = input("Port? ")
    ThreadedServer('',port_num).listen()
