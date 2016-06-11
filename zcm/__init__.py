#!/usr/bin/python

from operation_queue import TimerOperation, SubscriberOperation, ServerOperation, OperationQueue
from timer import Timer
from publisher import Publisher
from subscriber import Subscriber
from client import Client
from server import Server
from component import Component
from actor import Actor
import argparse

def main():
    """Entry point for the application script"""

    parser = argparse.ArgumentParser(description=\
                                     'functionality: Spawn a ZCM Actor', 
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--config', nargs='?', default=None, help='Name of configuration file')
    args = vars(parser.parse_args())

    if not (args['config'] == None):
        my_actor = Actor()
        my_actor.configure("configuration.json")
        my_actor.run()
