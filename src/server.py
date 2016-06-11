import zmq
from threading import Thread, Lock
from operation_queue import OperationQueue, ServerOperation

class Server():
    def __init__(self, name, priority, endpoints, operation_function, operation_queue):
        self.name = name
        self.priority = priority
        self.endpoints = endpoints
        self.operation_function = operation_function
        self.operation_queue = operation_queue
        self.context = zmq.Context()
        self.server_socket = self.context.socket(zmq.REP)
        for endpoint in self.endpoints:
            self.server_socket.bind(endpoint)
        self.ready = True
        self.func_mutex = Lock()

    def bind(self, new_endpoints):
        self.endpoints = new_endpoints
        self.context = zmq.Context()
        self.server_socket = self.context.socket(zmq.REP)
        for endpoint in self.endpoints:
            self.server_socket.bind(endpoint)
        self.ready = True

    def add_connection(self, new_connection):
        self.server_socket.bind(new_connection)
    
    def recv(self):
        while(True):
            while(self.ready == False):
                pass
            received_request = self.server_socket.recv()
            self.ready = False
            if (len(received_request) > 0):
                self.func_mutex.acquire()
                def bind(func, *args, **kwargs):
                    return lambda: func(*args, **kwargs)
                new_operation = ServerOperation(self.name, self.priority, 
                                                bind(self.operation_function, 
                                                     received_request),
                                                self)
                self.operation_queue.enqueue(new_operation)
                self.func_mutex.release()

    def rebind_operation_function(self, new_operation_function):
        self.func_mutex.acquire()
        self.operation_function = new_operation_function
        self.func_mutex.release()

    def spawn(self):
        return Thread(target = self.recv)

    def start(self):
        server_thread = self.spawn()
        server_thread.start()        
