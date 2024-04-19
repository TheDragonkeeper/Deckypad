import socket
import GamePad
import queue
import time
import threading

class Manage():
    def __init__(self):
        self.PORT = 9090
        self.HOST = "0.0.0.0"
        self.thread = None
        self.thread_sig = True
        self.connected = None
        self.sock = None
        self.clients = {}
        self.mode = -1
        self.queue = queue.Queue()


    def kill_thread(self):
        self.thread_sig = False
        # if self.thread != None:
        #     self.thread.join()S
        self.thread = None

    ########### HOST SECTION #####
    def start_host(self):
        self.connected = None
        self.thread = threading.Thread(target=self.server)
        self.thread.start()
        while self.connected == None:
            time.sleep(1)
        return self.connected

    def server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(0)
        self.connected = True
        self.mode = 1
        self.gamepad = GamePad.Gamepad()
        while self.thread_sig:
            client_socket, client_address = self.sock.accept()
            print("accepted client")
            self.queue.put([client_socket, client_address])
        self.mode = -1
        self.sock.close()
        self.sock = None


    def server_newclient(self, client_socket,client_address):
        client_name = str(client_address[0])+str(client_address[1])
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
        if not client_name in self.clients:
            self.clients[client_name] = {
                "socket": client_socket,
                "addr": client_address[0],
                "port": client_address[1]
            }
        while self.thread_sig:
            request = client_socket.recv(1024)
            request = request.decode("utf-8")
            if request.lower() == "close":
                self.gamepad.killpad("0")
                client_socket.send("closed".encode("utf-8"))
                break

            self.gamepad.handle_reciecved("0", request)

            response = "accepted".encode("utf-8")
            client_socket.send(response)
        try:
            self.gamepad.killpad("0")
        except: pass
        client_socket.close()
        print("Connection to client closed")
        self.clients.pop(client_name, None)

    ######################################################
    ################ Client Section ######################

    def start_client(self, ip, port):
        self.connected = None
        self.HOST = ip
        self.PORT = port
        self.thread = threading.Thread(target=self.client)
        self.thread.start()
        while self.connected == None:
            pass
        print("returning"+ str(self.connected))
        return self.connected

    def client(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST, self.PORT))
        self.connected = True
        self.mode = 0
        while self.thread_sig:
            response = self.sock.recv(1024)
            response = response.decode("utf-8")

            if response.lower() == "closed":
                break
        self.sock.close()
        self.mode = -1
        print("Connection to server closed")
        self.connected = False
        print("no connection")
    ########################################################

    def sent_joy_data(self, event):
        if self.mode == 0:
            #print(event.key)
            self.sock.send(str(event).encode())

    def send_message(self, message):
        self.sock.send(message.encode("utf-8")[:1024])
