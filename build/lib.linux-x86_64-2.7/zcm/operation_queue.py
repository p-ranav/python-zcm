#!/usr/bin/env python
"""operation_queue.py: This file contains classes for supported operation types & the component operation queue.
"""
from Queue import PriorityQueue
from threading import Thread, Lock
import zmq

__author__ = "Pranav Srinivas Kumar"
__copyright__ = "Copyright 2016, Pranav Srinivas Kumar"
__credits__ = ["Pranav Srinivas Kumar"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Pranav Srinivas Kumar"
__email__ = "pranav.srinivas.kumar@gmail.com"
__status__ = "Production"

# Timer Operation Class - This operation is created when ever a timer expires
class TimerOperation():
    def __init__(self, name, priority, operation_function):
        """
        Construct a timer operation
        
        Keyword arguments:
        name -- Name of the operation
        priority -- Priority of the operation
        operation_function -- Timer function
        """
        self.name = name
        self.priority = priority
        self.operation_function = operation_function

    def execute(self):
        """Execute the timer operation function i.e. the callback."""
        self.operation_function()

# Subscriber Operation class - This operation is created when a subscriber receives messages
class SubscriberOperation():
    def __init__(self, name, priority, operation_function):
        """
        Construct a subscriber operation
        
        Keyword arguments:
        name -- Name of the operation
        priority -- Priority of the operation
        operation_function -- Timer function
        """
        self.name = name
        self.priority = priority
        self.operation_function = operation_function

    def execute(self):
        """Execute the subscriber operation function i.e. the callback."""
        self.operation_function()

# Server Operation class - This operation is created when a server receives requests
class ServerOperation():
    def __init__(self, name, priority, operation_function, server):
        """
        Construct a subscriber operation
        
        Keyword arguments:
        name -- Name of the operation
        priority -- Priority of the operation
        operation_function -- Timer function
        server -- The server object used to reply to the client when the operation completes
        """
        self.name = name
        self.priority = priority
        self.operation_function = operation_function
        self.server = server

    def execute(self):
        """Execute the server operation function and respond back to the client."""
        response = self.operation_function()
        if not (self.server == None):
            if not (self.server.server_socket == None):
                self.server.server_socket.send(response)
        self.server.ready = True

# Operation Queue class - The component operation (priority) queue that holds operations
class OperationQueue():
    def __init__(self, queue_size = 1000):
        """
        Construct the priority queue and prepare a queue mutex

        Keyword arguments:
        queue_size - Size of the operation queue i.e. maximum number of operations
        """
        self.operation_queue = PriorityQueue(queue_size)
        self.queue_mutex = Lock()

    def enqueue(self, new_operation):
        """
        Enqueue a new operation onto the operation queue

        Keyword arguments:
        new_operation - New operation to be enqueued.
        """
        self.queue_mutex.acquire()
        self.operation_queue.put((new_operation.priority, new_operation))
        self.queue_mutex.release()

    def dequeue(self):
        """Dequeue the front operation from the operation queue."""
        return self.operation_queue.get()

    def empty(self):
        """Return true if the operation queue is empty; else return false."""
        return self.operation_queue.empty()

    def process(self):
        """Process the operation queue - Execute operations in the queue if queue not empty."""
        while(True):
            if (not self.operation_queue.empty()):
                self.queue_mutex.acquire()
                first_operation = self.dequeue()
                self.queue_mutex.release()
                first_operation[1].execute()

    def spawn(self):
        """Spawn the component executor thread that processes the queue."""
        return Thread(target = self.process)
