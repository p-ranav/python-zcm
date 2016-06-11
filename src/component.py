from operation_queue import OperationQueue
from timer import Timer
from publisher import Publisher
from subscriber import Subscriber
from client import Client
from server import Server

class Component():
    def __init__(self, operation_queue_size=10000):
        self.operation_queue = OperationQueue(operation_queue_size)     
        self.timers = []
        self.publishers = []
        self.subscribers = []
        self.clients = []
        self.servers = []
        self.timer_functions = {}
        self.subscriber_functions = {}
        self.server_functions = {}
        self.executor_thread = None

    def timer(self, timer_name):
        for timer in self.timers:
            if timer.name == timer_name:
                return timer
        return None

    def publisher(self, publisher_name):
        for publisher in self.publishers:
            if publisher.name == publisher_name:
                return publisher
        return None

    def subscriber(self, subscriber_name):
        for subscriber in self.subscribers:
            if subscriber.name == subscriber_name:
                return subscriber
        return None

    def client(self, client_name):
        for client in self.clients:
            if client.name == client_name:
                return client
        return None

    def server(self, server_name):
        for server in self.servers:
            if server.name == server_name:
                return server
        return None

    def add_timer(self, new_timer):
        self.timers.append(new_timer)

    def add_publisher(self, new_publisher):
        self.publishers.append(new_publisher)

    def add_subscriber(self, new_subscriber):
        self.subscribers.append(new_subscriber)

    def add_client(self, new_client):
        self.clients.append(new_client)

    def add_server(self, new_server):
        self.servers.append(new_server)

    def configure_publishers(self, publisher_dictionary):
        for key, value in publisher_dictionary.iteritems():
            this_publisher = self.publisher(key)
            if not (this_publisher == None):
                this_publisher.bind(value)

    def configure_subscribers(self, subscriber_dictionary):
        for key, value in subscriber_dictionary.iteritems():
            this_subscriber = self.subscriber(key)
            if not (this_subscriber == None):
                this_subscriber.connect(value)

    def configure_clients(self, client_dictionary):
        for key, value in client_dictionary.iteritems():
            this_client = self.client(key)
            if not (this_client == None):
                this_client.connect(value)

    def configure_servers(self, server_dictionary):
        for key, value in server_dictionary.iteritems():
            this_server = self.server(key)
            if not (this_server == None):
                this_server.bind(value)

    def register_timer_operation(self, operation_name, operation_function):
        self.timer_functions[operation_name] = operation_function

    def register_subscriber_operation(self, operation_name, operation_function):
        self.subscriber_functions[operation_name] = operation_function

    def register_server_operation(self, operation_name, operation_function):
        self.server_functions[operation_name] = operation_function

    def spawn(self):
        self.executor_thread = self.operation_queue.spawn()
        for timer in self.timers:
            timer.start()
        for subscriber in self.subscribers:
            subscriber.start()
        for server in self.servers:
            server.start()
        return self.executor_thread
    
