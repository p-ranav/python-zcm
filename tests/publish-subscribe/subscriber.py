from zcm import *

class SubscriberComponent(Component):
    def __init__(self):
        """Register a subscriber operation"""
        Component.__init__(self)
        self.register_subscriber_operation("subscriber_function",
                                           self.subscriber_function)

    def subscriber_function(self, message):
        print "Subscriber : Received Message:", message
