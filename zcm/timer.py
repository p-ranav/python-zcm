import sched, time
from threading import Thread, Lock
from operation_queue import OperationQueue, TimerOperation

class Timer():
    def __init__(self, name, priority, period, 
                 operation_function, operation_queue):
        self.name = name
        self.period = period
        self.priority = priority
        self.operation_function = operation_function
        self.operation_queue = operation_queue
        self.period_mutex = Lock()
        self.func_mutex = Lock()

    def operation(self):
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
        self.period_mutex.acquire()
        self.period = new_period
        self.period_mutex.release()

    def rebind_operation_function(self, new_operation_function):
        self.func_mutex.acquire()
        self.operation_function = new_operation_function
        self.func_mutex.release()

    def spawn(self):
        return Thread(target = self.operation)

    def start(self):
        timer_thread = self.spawn()
        timer_thread.start()

        
        
