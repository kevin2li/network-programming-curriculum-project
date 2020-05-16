"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from message import Message


class Server:
    def __init__(self, IP, PORT):
        self.clients = {}
        self.addresses = {}
        self.HOST = IP
        self.PORT = PORT
        self.BUFSIZE = 1024

    def establish(self):
        self.SERVER = socket(AF_INET, SOCK_STREAM)
        self.SERVER.bind((self.HOST, self.PORT))
        self.SERVER.listen(10)
        print("Waiting for connection...")
        self.ACCEPT_THREAD = Thread(target=self.accept_incoming_connections)
        self.ACCEPT_THREAD.start()
        self.ACCEPT_THREAD.join()
        self.SERVER.close()

    def accept_incoming_connections(self):
        """Sets up handling for incoming clients."""
        while True:
            client, client_address = self.SERVER.accept()
            print("%s:%s has connected." % client_address)
            msg = Message("welcome", "Greetings from the chatroom! enjoy your time!", "system")
            client.send(msg.serialize().encode(encoding="utf-8"))
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):  # Takes client socket as argument.
        """Handles a single client connection."""
        name = client.recv(self.BUFSIZE).decode("utf8")
        self.clients[client] = name
        msg = Message("join", name, "system")
        self.broadcast(msg, client)

        names = [k for k in self.clients.values()]
        print(names)
        msg = Message("member", str(names), "system")
        client.send(msg.serialize().encode(encoding="utf-8"))

        while True:
            msg = client.recv(self.BUFSIZE).decode("utf-8")
            print(msg)
            msg = Message.deserialize(msg)
            if msg.type != 'leave':
                self.broadcast(msg, client)
            else:
                msg = Message("leave", name, "system")
                self.broadcast(msg, client)
                del self.clients[client]
                client.close()

                names = [k for k in self.clients.values()]
                print(names)
                msg = Message("member", str(names), "system")
                self.broadcast(msg, "")
                break

    def broadcast(self, msg, src):
        """Broadcasts a message to all the clients."""
        for client in self.clients:
            if client != src:
                client.send(msg.serialize().encode(encoding="utf-8"))


if __name__ == '__main__':
    server = Server("127.0.0.1", 33000)
    server.establish()

