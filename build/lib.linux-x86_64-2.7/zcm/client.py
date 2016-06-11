#!/usr/bin/env python
"""client.py: This file contains the Client class."""
import zmq

__author__ = "Pranav Srinivas Kumar"
__copyright__ = "Copyright 2016, Pranav Srinivas Kumar"
__credits__ = ["Pranav Srinivas Kumar"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Pranav Srinivas Kumar"
__email__ = "pranav.srinivas.kumar@gmail.com"
__status__ = "Production"

# Client class
class Client():
    def __init__(self, name, endpoints = None):
        """
        Create a client

        Keyword arguments:
        name - Name of the timer
        endpoints - A list of endpoint strings
        """
        self.name = name
        self.endpoints = None
        self.context = None
        self.client_socket = None
        if not (endpoints == None):
            self.endpoints = endpoints
            self.context = zmq.Context()
            self.client_socket = self.context.socket(zmq.REQ)
            for endpoint in self.endpoints:
                self.client_socket.connect(endpoint)
    
    def connect(self, new_endpoints):
        """
        Connect this client to a new set of endpoints

        Keyword arguments:
        new_endpoints - New set of endpoints as a list
        """
        self.endpoints = new_endpoints
        self.context = zmq.Context()
        self.client_socket = self.context.socket(zmq.REQ)
        for endpoint in self.endpoints:
            self.client_socket.connect(endpoint)

    def call(self, message):
        """
        Call a server with a request message
        
        Keyword arguments:
        message - The message string. Serialize complex objects to strings with e.g. protobuf
        """
        self.client_socket.send(message)
        return self.client_socket.recv()

