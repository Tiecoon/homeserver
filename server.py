import socket
import threading
import time

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
            clients.append(["name",0,threading.Event()])
            threading.Thread(target = self.manage,args=
                    (clients,clients[len(clients)-1],
                        client,len(clients))).start()
            time.sleep(5)
            print(len(clients))
            clients[0][2].set()

    def manage(self,clients,sample,client,num):
        if self.listenToClient(sample, client) == "host":
            self.controller(sample,client,clients)
        if sample in clients:
            del clients[clients.index(sample)]
        else:
            print("something went wrong")
        return

    def controller(self,clientpair,client,clients):
        try:
            names = ""
            for i in clients:
                print(i[0])
                names+=i[0]
            client.send(names.encode())
            while True:
                data = client.recv(size)
                if not data: raise
                message = data.split(",")
                for i in clients:
                    if i[0] == data:

            return
        except:
            client.close()
            return

    def listenToClient(self, clientpair, client):
        size = 1024

        try:
            print(clientpair[0])
        #name
            data = client.recv(size)
            if not data: raise
            clientpair[0]=data.rstrip().decode()
            print(clientpair[0])
            if clientpair[0] == "control":
                print("host init")
                return "host"

            #state
            data = client.recv(size)
            if not data: raise
            clientpair[1]=data.rstrip()
            print(clientpair[1])
            print("waiting")
            clientpair[2].clear()
            clientpair[2].wait()
            print("event released")

            while True:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data
                    response = data
                    client.send(response)
                else:
                    raise error('Client disconnected')
        except:
            #remove on close
            print("delete")
            client.close()
            return

if __name__ == "__main__":
    port_num = input("Port? ")
    ThreadedServer('',port_num).listen()
