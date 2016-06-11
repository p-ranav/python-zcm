import zmq

class Client():
    def __init__(self, name, endpoints = None):
        self.name = name
        self.endpoints = None
        self.context = None
        self.client_socket = None
        if not (endpoints == None):
            self.endpoints = endpoints
            self.context = zmq.Context()
            self.client_socket = self.context.socket(zmq.REQ)
            for endpoint in self.endpoints:
                self.client_socket.connect(endpoint)
    
    def connect(self, new_endpoints):
        self.endpoints = new_endpoints
        self.context = zmq.Context()
        self.client_socket = self.context.socket(zmq.REQ)
        for endpoint in self.endpoints:
            self.client_socket.connect(endpoint)

    def call(self, message):
        self.client_socket.send(message)
        return self.client_socket.recv()

