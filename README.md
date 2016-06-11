ZeroMQ Component Model (ZCM) in Python
======================================

Overview
---------

* ZCM is a lightweight component model using ZeroMQ (http://zeromq.org/) 
* Components are the building blocks of an application
* Components are characterized by ports and timers. 
* Timers are bound to an *operation* and fire periodically
* There are four basic types of ports in ZCM: publisher, subscriber, client and server
* Publishers publish messages and Subscribers receive messages
* Clients request the services of a server by sending a request message; Servers receive such requests, process the requests, and respond back to the Client. Until the Server responds, the Client port blocks
* A Component can be instantiated multiple times in an application with different port configurations
* A component has a single operation queue that handles timer triggers and receives messages
* A component has an executor thread that processes this operation queue
* Components register functionality e.g. timer_operations, subscribers_operations etc. 
* Component instances are grouped together into a process, called *Actor*
* An actor receives a configuration (.JSON) file, that contains information regarding the components to instantiate
* This configuration file also contains properties of all timers and ports contained by the component instances

Python Packaging Index (PyPI) : https://pypi.python.org/pypi/zcm/1.0.0

Installation
-------------

```bash
$ pip install zcm
```

Simple Timer Example
--------------------

* Let's build a simple time-triggered application
* Prepare the application workspace:

```bash
$ mkdir simple-timer
$ cd simple-timer
$ touch __init__.py
```

* Create a simple timer component

```bash
$ touch simple_timer.py
```

* Edit simple_timer.py as shown below. 
* SimpleTimer has one functionality - "timer_function" that when called prints the current time
* This functionality is registered as an operation in the component's constructor

```python
from zcm import *
from time import gmtime, strftime

# Simple timer component
class SimpleTimer(Component):
    def __init__(self):
        Component.__init__(self)
        self.register_timer_operation("timer_function", 
                                      self.timer_function)

    def timer_function(self):
        print "Timer expired! Current Time: ",\
            strftime("%Y-%m-%d %H-%M-%S", gmtime())
```

