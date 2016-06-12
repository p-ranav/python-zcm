from zcm import *
import krpc

class ksp_rocket_controller(Component):
    def __init__(self):
        Component.__init__(self)

        # Register component timers
        self.register_timer_operation("sensor_timer_operation", 
                                      self.sensor_timer_operation)
        self.register_timer_operation("control_timer_operation", 
                                      self.control_timer_operation)

        # Prepare kRPC connection and obtain active vessel object
        self.krpc_connection = krpc.connect(name='KSP Rocket Controller', 
                                            address='192.168.198.1') 
        self.vessel = self.krpc_connection.space_center.active_vessel
        self.refframe = self.vessel.orbit.body.reference_frame
        self.flight = self.vessel.flight(self.refframe)
        self.vessel_parts = self.vessel.parts

        # Position is a tuple (float, float, float)
        self.position = self.krpc_connection.add_stream(self.vessel.position, 
                                                        self.refframe)

        # Velocity is a tuple (float, float, float)
        self.velocity = self.krpc_connection.add_stream(self.vessel.velocity, 
                                                        self.refframe)

        # Flight Telemetry
        self.latitude = self.flight.latitude
        self.longitude = self.flight.longitude
        self.surface_altitude = self.flight.surface_altitude
        self.g_force = self.flight.g_force
        self.pitch = self.flight.pitch
        self.heading = self.flight.heading
        self.roll = self.flight.roll
        self.direction = self.flight.direction

        # Flight Control Status
        self.control = self.vessel.control
        self.sas_state = self.control.sas
        self.rcs_state = self.control.rcs
        self.gear_state = self.control.gear
        self.lights_state = self.control.lights
        self.brakes_state = self.control.brakes
        self.throttle_state = self.control.throttle
        self.pitch_state = self.control.pitch
        self.yaw_state = self.control.yaw
        self.roll_state = self.control.roll

        self.meco_altitude = 1000
        self.parachute_altitude = 1300
        self.landing_gear_altitude = 200
        self.landing_altitude = 80

        self.current_state = "READY_FOR_LAUNCH"
        print "KSP ROCKET CONTROLLER:"
        print "---------------------"
        print "LOG ENTRY : Ready for Launch"

    def sensor_timer_operation(self):
        # Flight Telemetry
        self.latitude = self.flight.latitude
        self.longitude = self.flight.longitude
        self.surface_altitude = self.flight.surface_altitude
        self.g_force = self.flight.g_force
        self.pitch = self.flight.pitch
        self.heading = self.flight.heading
        self.roll = self.flight.roll
        self.direction = self.flight.direction

        # Flight Control Status
        self.control = self.vessel.control
        self.sas_state = self.control.sas
        self.rcs_state = self.control.rcs
        self.gear_state = self.control.gear
        self.lights_state = self.control.lights
        self.brakes_state = self.control.brakes
        self.throttle_state = self.control.throttle
        self.pitch_state = self.control.pitch
        self.yaw_state = self.control.yaw
        self.roll_state = self.control.roll

    def control_timer_operation(self):

        if (self.current_state == "READY_FOR_LAUNCH"):
            self.control.throttle = 1
            self.control.sas = True
            self.control.rcs = True
            self.control.gear = False
            self.control.activate_next_stage()
            self.current_state = "LAUNCH_SUCCESS"
            print "LOG ENTRY : Launch Successful"

        elif (self.current_state == "LAUNCH_SUCCESS"):
            if (self.vessel.thrust == 0 or self.surface_altitude > self.meco_altitude):
                self.control.throttle = 0
                self.current_state = "MAIN_ENGINE_CUTOFF"
                print "LOG ENTRY : Main Engine Cutoff"

        elif (self.current_state == "MAIN_ENGINE_CUTOFF"):
            if (self.flight.vertical_speed <= 0):
                self.current_state = "APOGEE_REACHED"
                print "LOG ENTRY : Apogee Reached"

        elif (self.current_state == "APOGEE_REACHED" and
              self.surface_altitude >= self.parachute_altitude):
            self.current_state = "PREPARE_FOR_LANDING"
            print "LOG ENTRY : Prepare for Landing"

        elif (self.surface_altitude < self.parachute_altitude and 
              self.current_state == "PREPARE_FOR_LANDING"):
            self.parachutes = self.vessel_parts.parachutes
            for parachute in self.parachutes:
                parachute.deploy()
            if (self.surface_altitude < self.landing_gear_altitude):
                self.control.gear = True
            if (self.surface_altitude < self.landing_altitude):
                self.current_state = "RECOVERY_SUCCESSFUL"
                print "LOG ENTRY : Recovery Successful"
                print "LOG ENTRY : Mission Complete"
        else:
            pass
            

