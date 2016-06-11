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
