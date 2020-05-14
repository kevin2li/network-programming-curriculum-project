"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import json
from message import Message


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        msg = Message("welcome", "Greetings from the chatroom! enjoy your time!", "system")

        client.send(msg.serialize().encode(encoding="utf-8"))

        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    clients[client] = name
    # welcome = 'Welcome %s! Now you can chat with others.' % name
    # client.send(bytes(welcome, "utf8"))

    # msg = "<system> %s has joined the chat!" % name
    msg = Message("join", name, "system")
    broadcast(msg, client)

    names = [k for k in clients.values()]
    print(names)
    msg = Message("member", str(names), "system")
    client.send(msg.serialize().encode(encoding="utf-8"))

    while True:
        msg = client.recv(BUFSIZ).decode("utf-8")
        print(msg)
        msg = Message.deserialize(msg)
        if msg.type != 'leave':
            broadcast(msg, client)
        else:
            msg = Message("leave", name, "system")
            broadcast(msg, client)
            del clients[client]
            client.close()

            names = [k for k in clients.values()]
            print(names)
            msg = Message("member", str(names), "system")
            broadcast(msg, "")
            break


def broadcast(msg, src):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for client in clients:
        if client != src:
            client.send(msg.serialize().encode(encoding="utf-8"))


clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
