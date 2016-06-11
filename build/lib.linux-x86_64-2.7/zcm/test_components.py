from component import Component

class component_1(Component):
    def __init__(self):
        Component.__init__(self)
        self.register_timer_operation("timer_1_function", 
                                      self.timer_1_function)
        self.register_subscriber_operation("subscriber_function",
                                           self.subscriber_function)

    def timer_1_function(self):
        self.publisher("publisher_port").send("Component_1")
        print "Component 1 : Timer : Published message: Component_1"

    def subscriber_function(self, received_message):
        print "Component 1 : Subscriber : Received message:", received_message 


class component_2(Component):
    def __init__(self):
        Component.__init__(self)
        self.register_timer_operation("timer_function",
                                      self.timer_function)
        self.register_server_operation("server_function",
                                       self.server_function)

    def timer_function(self):
        self.publisher("publisher_port").send("Component_2")
        print "Component_2 : Timer : Published message: Component_2"

    def server_function(self, received_request):
        print "Component_2 : Server : Received request:", received_request
        self.publisher("publisher_port").send("Component_2")
        print "Component_2 : Server : Published message: Component_2"
        return "Component_2"

class component_3(Component):
    def __init__(self):
        Component.__init__(self)
        self.register_timer_operation("timer_function", self.timer_function)

    def timer_function(self):
        response = self.client("client_port").call("Component_3")
        print "Component_3 : Timer : Called Component_2::Server : Received : ", response
