import zmq
from threading import Thread, Lock
from operation_queue import SubscriberOperation, OperationQueue

class Subscriber():
    def __init__(self, name, priority, subscriber_filter, endpoints, 
                 operation_function, operation_queue):
        self.name = name
        self.priority = priority
        self.subscriber_filter = subscriber_filter
        self.endpoints = endpoints
        self.operation_function = operation_function
        self.operation_queue = operation_queue

        self.context = zmq.Context()
        self.subscriber_socket = self.context.socket(zmq.SUB)
        for endpoint in endpoints:
            self.subscriber_socket.connect(endpoint)
        self.subscriber_socket.setsockopt_string(zmq.SUBSCRIBE, self.subscriber_filter)      
        self.func_mutex = Lock()

    def connect(self, new_endpoints):
        self.endpoints = new_endpoints
        self.context = zmq.Context()
        self.subscriber_socket = self.context.socket(zmq.SUB)
        for endpoint in new_endpoints:
            self.subscriber_socket.connect(endpoint)
        self.subscriber_socket.setsockopt_string(zmq.SUBSCRIBE, self.subscriber_filter)        

    def add_connection(self, new_connection):
        self.subscriber_socket.connect(new_connection)

    def recv(self):
        while(True):
            received_message = self.subscriber_socket.recv()
            if (len(received_message) > 0):
                self.func_mutex.acquire()
                def bind(func, *args, **kwargs):
                    return lambda: func(*args, **kwargs)
                new_operation = SubscriberOperation(self.name, self.priority, 
                                                    bind(self.operation_function, 
                                                         received_message))
                self.operation_queue.enqueue(new_operation)
                self.func_mutex.release()

    def rebind_operation_function(self, new_operation_function):
        self.func_mutex.acquire()
        self.operation_function = new_operation_function
        self.func_mutex.release()

    def spawn(self):
        return Thread(target = self.recv)

    def start(self):
        subscriber_thread = self.spawn()
        subscriber_thread.start()        
