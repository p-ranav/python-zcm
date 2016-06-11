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

from client import Client
from timer import Timer
from operation_queue import OperationQueue

my_client = Client("my_client", ["tcp://127.0.0.1:5510"])

def timer_operation():
    global my_client
    message = "59265926952"
    print "CLIENT:: Calling server with message: ", message
    reply = my_client.call(message)
    print "CLIENT:: Received reply", reply

def server_operation(message):
    print "SERVER:: Received request: ", message 
    reply = "2075072606720"
    print "SERVER:: Responding to client with: ", reply
    return reply

ClientQueue = OperationQueue(1000) # Queue max size = 1000
ServerQueue = OperationQueue(1000)

timer = Timer("Timer", 90, 1.0, timer_operation, ClientQueue)
server = Server("Server", 70, 
                ["tcp://*:5510"], 
                server_operation, ServerQueue)

client_executor_thread = ClientQueue.spawn()
server_executor_thread = ServerQueue.spawn()
client_executor_thread.start()
server_executor_thread.start()
server.start()
timer.start()
