#!/usr/bin/env python
"""subscriber.py: This file contains the Subscriber class."""
import zmq
from threading import Thread, Lock
from operation_queue import SubscriberOperation, OperationQueue

__author__ = "Pranav Srinivas Kumar"
__copyright__ = "Copyright 2016, Pranav Srinivas Kumar"
__credits__ = ["Pranav Srinivas Kumar"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Pranav Srinivas Kumar"
__email__ = "pranav.srinivas.kumar@gmail.com"
__status__ = "Production"

# Subscriber class
class Subscriber():
    def __init__(self, name, priority, subscriber_filter, endpoints, 
                 operation_function, operation_queue):
        """
        Create a subscriber

        Keyword arguments:
        name - Name of the timer
        priority - Priority of the subscriber
        subscriber_filter - ZMQ filter for the subscriber
        endpoints - A list of endpoint strings
        operation_function - Operation function of the subscriber
        operation_queue - The operation queue object
        """
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
        """
        Connect to a new set of endpoints

        Keyword arguments:
        new_endpoints - A new set of endpoints to connect to
        """
        self.endpoints = new_endpoints
        self.context = zmq.Context()
        self.subscriber_socket = self.context.socket(zmq.SUB)
        for endpoint in new_endpoints:
            self.subscriber_socket.connect(endpoint)
        self.subscriber_socket.setsockopt_string(zmq.SUBSCRIBE, self.subscriber_filter)        

    def add_connection(self, new_connection):
        """
        Add a new endpoint
        
        Keyword arguments:
        new_connection - New connection address to connect to
        """
        self.subscriber_socket.connect(new_connection)

    def recv(self):
        """
        Thread function of the susbcriber

        Behavior:
        (1) Wait for a new message on the subscriber zmq socket
        (2) Create a subscriber operation
        (3) Enqueue onto the operation queue
        (4) Goto step (1)
        """
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
        """
        Rebind the subscriber operation function
        
        Keyword arguments:
        new_operation_function - New subscriber function to be handled upon recv()
        """
        self.func_mutex.acquire()
        self.operation_function = new_operation_function
        self.func_mutex.release()

    def spawn(self):
        """Spawn a new thread for the subscriber."""        
        return Thread(target = self.recv)

    def start(self):
        """Start the subscriber thread."""
        subscriber_thread = self.spawn()
        subscriber_thread.start()        
