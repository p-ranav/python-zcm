from zcm import *

class ServerComponent(Component):
    def __init__(self):
        """Register the server operation"""
        Component.__init__(self)
        self.register_server_operation("server_function", 
                                       self.server_function)

    def server_function(self, request):
        """Receive requests and respond to remote clients"""
        print "Server : Received message:", request 
        return "ACK"



