import json
from pprint import pprint
import importlib

class Actor():
    def __init__(self):
        self.component_instances = []

    def configure(self, configuration_file):
        with open(configuration_file) as data_file:
            root = json.load(data_file)
            pprint(root)
            for instance in root["Component Instances"]:
                instance_source = instance["Definition"]
                module_name, class_name = instance_source.split(".") 
                module = importlib.import_module(module_name) 
                component_instance = getattr(module, class_name)() 

                publishers_config_map = {}
                subscribers_config_map = {}
                clients_config_map = {}
                servers_config_map = {}
                
                ## Finish configuration and you'll be done

    def run(self):
        for instance in self.component_instances:
            instance_thread = instance.spawn()
            instance_thread.start()

my_actor = Actor()
my_actor.configure("configuration.json")
