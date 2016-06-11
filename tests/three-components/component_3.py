from zcm import *

class Component_3(Component):
    def __init__(self):
        Component.__init__(self)
        self.register_timer_operation("timer_function", self.timer_function)
        
    def timer_function(self):
        response = self.client("client_port").call("Component_3")
        print "Component_3 : Timer : Called Component_2::Server : Received:", response
