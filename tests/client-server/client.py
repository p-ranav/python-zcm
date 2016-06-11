from zcm import *

class ClientComponent(Component):
    def __init__(self):
        """Register a timer operation"""
        Component.__init__(self)
        self.register_timer_operation("timer_function", 
                                      self.timer_function)

    def timer_function(self):
        """Request the services of a remote server using the client_port"""
        print "Client Timer : Sending message: client_timer_message" 
        response = self.client("client_port").call("client_timer_message")
        print "Client Timer : Received response :", response
