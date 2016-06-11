#!/usr/bin/env python
"""component.py: This file contains the Component class."""
from operation_queue import OperationQueue
from timer import Timer
from publisher import Publisher
from subscriber import Subscriber
from client import Client
from server import Server

__author__ = "Pranav Srinivas Kumar"
__copyright__ = "Copyright 2016, Pranav Srinivas Kumar"
__credits__ = ["Pranav Srinivas Kumar"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Pranav Srinivas Kumar"
__email__ = "pranav.srinivas.kumar@gmail.com"
__status__ = "Production"

# Component class
class Component():
    def __init__(self, operation_queue_size=10000):
        """Construct a component - Prepare the operation queue"""
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
        """Return a component timer by name"""
        for timer in self.timers:
            if timer.name == timer_name:
                return timer
        return None

    def publisher(self, publisher_name):
        """Return a component publisher by name"""
        for publisher in self.publishers:
            if publisher.name == publisher_name:
                return publisher
        return None

    def subscriber(self, subscriber_name):
        """Return a component subscriber by name"""
        for subscriber in self.subscribers:
            if subscriber.name == subscriber_name:
                return subscriber
        return None

    def client(self, client_name):
        """Return a component client by name"""
        for client in self.clients:
            if client.name == client_name:
                return client
        return None

    def server(self, server_name):
        """Return a component server by name"""
        for server in self.servers:
            if server.name == server_name:
                return server
        return None

    def add_timer(self, new_timer):
        """Add a new timer to this component"""
        self.timers.append(new_timer)

    def add_publisher(self, new_publisher):
        """Add a new publisher to this component"""
        self.publishers.append(new_publisher)

    def add_subscriber(self, new_subscriber):
        """Add a new subscriber to this component"""
        self.subscribers.append(new_subscriber)

    def add_client(self, new_client):
        """Add a new client to this component"""
        self.clients.append(new_client)

    def add_server(self, new_server):
        """Add a new server to this component"""
        self.servers.append(new_server)

    def configure_publishers(self, publisher_dictionary):
        """Configure all component publishers"""
        for key, value in publisher_dictionary.iteritems():
            this_publisher = self.publisher(key)
            if not (this_publisher == None):
                this_publisher.bind(value)

    def configure_subscribers(self, subscriber_dictionary):
        """Configure all component subscribers"""
        for key, value in subscriber_dictionary.iteritems():
            this_subscriber = self.subscriber(key)
            if not (this_subscriber == None):
                this_subscriber.connect(value)

    def configure_clients(self, client_dictionary):
        """Configure all component clients"""
        for key, value in client_dictionary.iteritems():
            this_client = self.client(key)
            if not (this_client == None):
                this_client.connect(value)

    def configure_servers(self, server_dictionary):
        """Configure all component servers"""
        for key, value in server_dictionary.iteritems():
            this_server = self.server(key)
            if not (this_server == None):
                this_server.bind(value)

    def register_timer_operation(self, operation_name, operation_function):
        """Register a timer operation"""
        self.timer_functions[operation_name] = operation_function

    def register_subscriber_operation(self, operation_name, operation_function):
        """Register a subscriber operation"""
        self.subscriber_functions[operation_name] = operation_function

    def register_server_operation(self, operation_name, operation_function):
        """Register a server operation"""
        self.server_functions[operation_name] = operation_function

    def spawn(self):
        """Spawn the component executor thread and all port-specific threads"""
        self.executor_thread = self.operation_queue.spawn()
        for timer in self.timers:
            timer.start()
        for subscriber in self.subscribers:
            subscriber.start()
        for server in self.servers:
            server.start()
        return self.executor_thread
    
