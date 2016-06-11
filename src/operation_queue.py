from Queue import PriorityQueue
from threading import Thread, Lock
import zmq

class TimerOperation():
    def __init__(self, name, priority, operation_function):
        self.name = name
        self.priority = priority
        self.operation_function = operation_function

    def execute(self):
        self.operation_function()

class SubscriberOperation():
    def __init__(self, name, priority, operation_function):
        self.name = name
        self.priority = priority
        self.operation_function = operation_function

    def execute(self):
        self.operation_function()

class ServerOperation():
    def __init__(self, name, priority, operation_function, server):
        self.name = name
        self.priority = priority
        self.operation_function = operation_function
        self.server = server

    def execute(self):
        response = self.operation_function()
        if not (self.server == None):
            if not (self.server.server_socket == None):
                self.server.server_socket.send(response)
        self.server.ready = True

class OperationQueue():

    def __init__(self, queue_size = 100):
        self.operation_queue = PriorityQueue(queue_size)
        self.queue_mutex = Lock()

    def enqueue(self, new_operation):
        self.queue_mutex.acquire()
        self.operation_queue.put((new_operation.priority, new_operation))
        self.queue_mutex.release()

    def dequeue(self):
        return self.operation_queue.get()

    def empty(self):
        return self.operation_queue.empty()

    def process(self):
        while(True):
            if (not self.operation_queue.empty()):
                self.queue_mutex.acquire()
                first_operation = self.dequeue()
                self.queue_mutex.release()
                first_operation[1].execute()

    def spawn(self):
        return Thread(target = self.process)
