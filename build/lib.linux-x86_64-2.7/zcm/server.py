#!/usr/bin/env python
"""server.py: This file contains the Server class."""
import zmq
from threading import Thread, Lock
from operation_queue import OperationQueue, ServerOperation

__author__ = "Pranav Srinivas Kumar"
__copyright__ = "Copyright 2016, Pranav Srinivas Kumar"
__credits__ = ["Pranav Srinivas Kumar"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Pranav Srinivas Kumar"
__email__ = "pranav.srinivas.kumar@gmail.com"
__status__ = "Production"

# Server class
class Server():
    def __init__(self, name, priority, endpoints, 
                 operation_function, operation_queue):
        """
        Create a server

        Keyword arguments:
        name - Name of the timer
        priority - Priority of the subscriber
        endpoints - A list of endpoint strings
        operation_function - Operation function of the subscriber
        operation_queue - The operation queue object
        """
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
        """
        Bind to a new set of endpoints

        Keyword arguments:
        new_endpoints - A new set of endpoints to connect to
        """
        self.endpoints = new_endpoints
        self.context = zmq.Context()
        self.server_socket = self.context.socket(zmq.REP)
        for endpoint in self.endpoints:
            self.server_socket.bind(endpoint)
        self.ready = True

    def add_connection(self, new_connection):
        """
        Add a new endpoint
        
        Keyword arguments:
        new_connection - New connection address to connect to
        """
        self.server_socket.bind(new_connection)
    
    def recv(self):
        """
        Thread function of the server

        Behavior:
        (1) Wait for a new request on the server zmq socket
        (2) Create a server operation
        (3) Enqueue onto the operation queue
        (4) Goto step (1)
        """
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
        """
        Rebind the subscriber operation function
        
        Keyword arguments:
        new_operation_function - New server function to be handled upon recv()
        """
        self.func_mutex.acquire()
        self.operation_function = new_operation_function
        self.func_mutex.release()

    def spawn(self):
        """Spawn a new thread for the server."""        
        return Thread(target = self.recv)

    def start(self):
        """Start the server thread."""
        server_thread = self.spawn()
        server_thread.start()        
