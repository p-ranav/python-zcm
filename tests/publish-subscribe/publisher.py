from zcm import *

class PublisherComponent(Component):
    def __init__(self):
        """Register a timer operation"""
        Component.__init__(self)
        self.register_timer_operation("timer_1_function",
                                      self.timer_1_function)

    def timer_1_function(self):
        self.publisher("timer_pub_1").send("timer_1_message")
        print "Publisher : Published message: timer_1_message"

