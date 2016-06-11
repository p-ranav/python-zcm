from zcm import *

class TimersComponent(Component):
    def __init__(self):
        """Register all timer operations"""
        Component.__init__(self)
        self.register_timer_operation("timer_1_function", self.timer_1_function)
        self.register_timer_operation("timer_2_function", self.timer_2_function)
        self.register_timer_operation("timer_3_function", self.timer_3_function)
        self.register_timer_operation("timer_4_function", self.timer_4_function)
        self.register_timer_operation("timer_5_function", self.timer_5_function)

    def timer_1_function(self):
        print "Timer 1 expiry handled" 

    def timer_2_function(self):
        print "Timer 2 expiry handled" 

    def timer_3_function(self):
        print "Timer 3 expiry handled" 

    def timer_4_function(self):
        print "Timer 4 expiry handled" 

    def timer_5_function(self):
        print "Timer 5 expiry handled" 
