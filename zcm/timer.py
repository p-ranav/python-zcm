#!/usr/bin/env python
"""timer.py: This file contains the Timer class."""
import sched, time
from threading import Thread, Lock
from operation_queue import OperationQueue, TimerOperation

__author__ = "Pranav Srinivas Kumar"
__copyright__ = "Copyright 2016, Pranav Srinivas Kumar"
__credits__ = ["Pranav Srinivas Kumar"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Pranav Srinivas Kumar"
__email__ = "pranav.srinivas.kumar@gmail.com"
__status__ = "Production"

# Timer class - Create a periodic timer and bind the timer to a callback operation
class Timer():
    def __init__(self, name, priority, period, 
                 operation_function, operation_queue):
        """
        Create a timer

        Keyword arguments:
        name - Name of the timer
        priority - Priority of the timer
        period - Period of the timer (in seconds)
        operation_function - Operation to which the timer is bound
        operation_queue - The operation queue object
        """
        self.name = name
        self.period = period
        self.priority = priority
        self.operation_function = operation_function
        self.operation_queue = operation_queue
        self.period_mutex = Lock()
        self.func_mutex = Lock()

    def operation(self):
        """
        Timer thread function

        Behavior:
        (1) Wait for timer expiry
        (2) Create a timer operation
        (3) Enqueue onto operation_queue
        (4) Goto step (1)
        """
        while(True):
            self.period_mutex.acquire()
            start = time.time()
            while((time.time() - start) < self.period):
                pass
            self.period_mutex.release()
                
            self.func_mutex.acquire()
            new_operation = TimerOperation(self.name, self.priority, 
                                           self.operation_function)
            self.operation_queue.enqueue(new_operation)
            self.func_mutex.release()
            
    def change_period(self, new_period):
        """
        Change the timer period

        Keyword arguments:
        new_period - New timer period in seconds
        """
        self.period_mutex.acquire()
        self.period = new_period
        self.period_mutex.release()

    def rebind_operation_function(self, new_operation_function):
        """
        Rebind the timer operation function

        Keyword arguments:
        new_operation_function - New timer function to handle timer expiry
        """        
        self.func_mutex.acquire()
        self.operation_function = new_operation_function
        self.func_mutex.release()

    def spawn(self):
        """Spawn a new thread for the timer."""
        return Thread(target = self.operation)

    def start(self):
        """Start the timer thread."""
        timer_thread = self.spawn()
        timer_thread.start()

        
        
