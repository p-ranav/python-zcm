#!/usr/bin/env python
"""actor.py: This file contains the Actor class."""
import json
import importlib
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

# Actor class
class Actor():
    def __init__(self):
        """Construct an actor - Prepare an empty list of component instances"""
        self.component_instances = []

    def configure(self, configuration_file):
        """
        Configure the component instances list
        
        Keyword arguments:
        configuration_file - JSON configuration file to parse
        """
        with open(configuration_file) as data_file:
            root = json.load(data_file)
            for instance in root["Component Instances"]:
                instance_source = instance["Definition"]
                module_name, class_name = instance_source.split(".") 
                module = importlib.import_module(module_name) 
                component_instance = getattr(module, class_name)() 

                publishers_config_map = {}
                subscribers_config_map = {}
                clients_config_map = {}
                servers_config_map = {}

                if "Timers" in instance.keys():
                    for timer in instance["Timers"]:
                        timer_name = timer["Name"]
                        timer_priority = timer["Priority"]
                        timer_period = timer["Period"]
                        timer_operation = timer["Function"]
                        new_timer = Timer(timer_name,
                                          timer_priority,
                                          timer_period,
                                          component_instance.timer_functions[timer_operation],
                                          component_instance.operation_queue)
                        component_instance.add_timer(new_timer)

                if "Publishers" in instance.keys():
                    for publisher in instance["Publishers"]:
                        publisher_name = publisher["Name"]
                        for endpoint in publisher["Endpoints"]:                        
                            if publisher_name not in publishers_config_map.keys():
                                publishers_config_map[publisher_name] = []
                                publishers_config_map[publisher_name].append(endpoint)
                                new_publisher = Publisher(publisher_name)
                                component_instance.add_publisher(new_publisher)

                if "Subscribers" in instance.keys():
                    for subscriber in instance["Subscribers"]:
                        subscriber_name = subscriber["Name"]
                        subscriber_priority = subscriber["Priority"]
                        subscriber_filter = subscriber["Filter"]
                        subscriber_operation = subscriber["Function"]
                        for endpoint in subscriber["Endpoints"]:
                            if subscriber_name not in subscribers_config_map.keys():
                                subscribers_config_map[subscriber_name] = []
                                subscribers_config_map[subscriber_name].append(endpoint)
                                new_subscriber = Subscriber(subscriber_name,
                                                            subscriber_priority,
                                                            subscriber_filter,
                                                            subscribers_config_map[subscriber_name],
                                                            component_instance.\
                                                            subscriber_functions[subscriber_operation],
                                                            component_instance.operation_queue)
                                component_instance.add_subscriber(new_subscriber)

                if "Clients" in instance.keys():
                    for client in instance["Clients"]:
                        client_name = client["Name"]
                        for endpoint in client["Endpoints"]:
                            if client_name not in clients_config_map.keys():
                                clients_config_map[client_name] = []
                                clients_config_map[client_name].append(endpoint)
                                new_client = Client(client_name)
                                component_instance.add_client(new_client)

                if "Servers" in instance.keys():
                    for server in instance["Servers"]:
                        server_name = server["Name"]
                        server_priority = server["Priority"]
                        server_operation = server["Function"]
                        for endpoint in server["Endpoints"]:
                            if server_name not in servers_config_map.keys():
                                servers_config_map[server_name] = []
                                servers_config_map[server_name].append(endpoint)
                                new_server = Server(server_name,
                                                    server_priority,
                                                    servers_config_map[server_name],
                                                    component_instance.server_functions[server_operation],
                                                    component_instance.operation_queue)
                                component_instance.add_server(new_server)

                component_instance.configure_publishers(publishers_config_map)
                component_instance.configure_subscribers(subscribers_config_map)
                component_instance.configure_clients(clients_config_map)
                component_instance.configure_servers(servers_config_map)
                self.component_instances.append(component_instance)

    def run(self):
        """Spawn all component instances"""
        for instance in self.component_instances:
            instance_thread = instance.spawn()
            instance_thread.start()
