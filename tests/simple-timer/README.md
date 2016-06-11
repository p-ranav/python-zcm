Simple Timer Example
--------------------

* Let's build a simple time-triggered application
* Prepare the application workspace:

```bash
$ mkdir simple-timer
$ cd simple-timer
$ touch __init__.py
```

* Create a simple timer component

```bash
$ touch simple_timer.py
```

* Edit simple_timer.py as shown below. 
* SimpleTimer has one functionality - "timer_function" that when called prints the current time
* This functionality is registered as an operation in the component's constructor

```python
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
```

* Now that the component is ready, let's prepare a configuration for this component
* We want to create an instance of this component definition
* We also want the component functionality, specifically the "timer_function" to be triggered by a timer
* Create a configuration file in the application workspace, as below:

```json
{
    "Component Instances": [
	{
	    "Name" : "simple_timer_component_instance",

	    "Definition" : "simple_timer.SimpleTimer",

	    "Timers" : [
		{
		    "Name" : "simple_timer",
		    "Priority" : 50,
		    "Period" : 5.0,
		    "Function" : "timer_function"
		}
	    ]	    
	}
    ]
}
```

* The above file creates an instance of the SimpleTimer class
* The configuration also adds a timer, "simple_timer", to this component
* This timer has a period of 5.0 seconds, and a priority of 50
* The priority is used when other component functions are concurrently triggered
* Now the workspace should contain: 
  > simple_timer.py
  > __init__.py
  > configuration.json

* Assuming, zcm has been installed, simply run:

```bash
$ zcm --config configuration.json
```

* You should see something like this: 

```bash
kelsier@luthadel:~/G/p/t/simple-timer|master⚡?                                                                                                                                                            
➤ zcm --config configuration.json 
Timer expired! Current Time:  2016-06-11 17-21-58
Timer expired! Current Time:  2016-06-11 17-22-03
Timer expired! Current Time:  2016-06-11 17-22-08
Timer expired! Current Time:  2016-06-11 17-22-13
Timer expired! Current Time:  2016-06-11 17-22-18
Timer expired! Current Time:  2016-06-11 17-22-23
Timer expired! Current Time:  2016-06-11 17-22-28
Timer expired! Current Time:  2016-06-11 17-22-33
Timer expired! Current Time:  2016-06-11 17-22-38
Timer expired! Current Time:  2016-06-11 17-22-43
Timer expired! Current Time:  2016-06-11 17-22-48
Timer expired! Current Time:  2016-06-11 17-22-53
Timer expired! Current Time:  2016-06-11 17-22-58
Timer expired! Current Time:  2016-06-11 17-23-03
Timer expired! Current Time:  2016-06-11 17-23-08
Timer expired! Current Time:  2016-06-11 17-23-13
```

* That's it! We just made a periodically triggered component