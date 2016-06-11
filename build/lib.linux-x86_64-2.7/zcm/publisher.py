#!/usr/bin/env python
"""publisher.py: This file contains the Publisher class."""
import zmq

__author__ = "Pranav Srinivas Kumar"
__copyright__ = "Copyright 2016, Pranav Srinivas Kumar"
__credits__ = ["Pranav Srinivas Kumar"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Pranav Srinivas Kumar"
__email__ = "pranav.srinivas.kumar@gmail.com"
__status__ = "Production"

# Publisher class
class Publisher():
    def __init__(self, name, endpoints = None):
        """
        Create a publisher

        Keyword arguments:
        name - Name of the timer
        endpoints - A list of endpoint strings
        """
        self.name = name
        self.endpoints = None
        self.context = None
        self.publisher_socket = None
        if not (endpoints == None):
            self.endpoints = endpoints
            self.context = zmq.Context()
            self.publisher_socket = self.context.socket(zmq.PUB)
            for endpoint in self.endpoints:
                self.publisher_socket.bind(endpoint)

    def bind(self, new_endpoints):
        """
        Bind the publisher to a new set of endpoints

        Keyword arguments:
        new_endpoints - New set of endpoints as a list
        """
        self.endpoints = new_endpoints
        self.context = zmq.Context()
        self.publisher_socket = self.context.socket(zmq.PUB)
        for endpoint in new_endpoints:
            self.publisher_socket.bind(endpoint)

    def add_connection(self, new_connection):
        """
        Add a new endpoint to the publisher

        Keyword arguments:
        new_connection - New endpoint to bind to
        """
        self.publisher_socket.bind(new_connection)

    def send(self, message):
        """
        Publish a new message
        
        Keyword arguments:
        message - The message string. Serialize complex objects to strings with e.g. protobuf
        """
        self.publisher_socket.send(message)
