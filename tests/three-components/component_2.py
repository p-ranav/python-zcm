from zcm import *

class Component_2(Component):
    def __init__(self):
        Component.__init__(self)
        self.register_timer_operation("timer_function", self.timer_function)
        self.register_server_operation("server_function", self.server_function)

    def timer_function(self):
        self.publisher("publisher_port").send("Component_2")
        print "Component_2 : Timer : Published Message : Component_2"

    def server_function(self, received_request):
        print "Component_2 : Server : Received message:", received_request
        self.publisher("publisher_port").send("Component_2")
        print "Component_2 : Server : Published message : Component_2"
        return "Component_2_ACK"
