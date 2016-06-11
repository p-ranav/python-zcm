from zcm import *

class Component_1(Component):
    def __init__(self):
        Component.__init__(self)
        self.register_timer_operation("timer_1_function", self.timer_1_function)
        self.register_subscriber_operation("subscriber_function", self.subscriber_function)

    def timer_1_function(self):
        self.publisher("publisher_port").send("Component_1")
        print "Component_1 : Timer : Published message : Component_1"

    def subscriber_function(self, received_message):
        print "Component_1 : Subscriber : Received message:", received_message
