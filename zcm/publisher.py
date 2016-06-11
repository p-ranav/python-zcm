import zmq

class Publisher():
    def __init__(self, name, endpoints = None):
        self.name = name
        self.endpoints = None
        self.context = None
        self.publisher_socket = None
        if not (endpoints == None):
            self.endpoints = endpoints
            self.context = zmq.Context()
            self.publisher_socket = self.context.socket(zmq.PUB)
            for endpoint in self.endpoints:
                self.publisher_socket.bind(endpoint)

    def bind(self, new_endpoints):
        self.endpoints = new_endpoints
        self.context = zmq.Context()
        self.publisher_socket = self.context.socket(zmq.PUB)
        for endpoint in new_endpoints:
            self.publisher_socket.bind(endpoint)

    def add_connection(self, new_connection):
        self.publisher_socket.bind(new_connection)

    def send(self, message):
        self.publisher_socket.send(message)
