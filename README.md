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

python-zcm is a Python port of https://github.com/pranav-srinivas-kumar/zcm

Installation
-------------

```bash
$ pip install zcm
```
