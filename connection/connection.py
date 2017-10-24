from abc import ABCMeta, abstractmethod


class Connection():
    __metaclass__ = ABCMeta

    def __init__(self):
        # every connection type will have a set of listeners
        # this is a dictionary, keyed by listener type
        self._message_listeners = {}

    def on_message(self, name):
        """
        decorator for being able to add a listener for a specific message type

        e.g. on how you would use in in the drone class, where you have created
        a variable 'conn = Connection()'

        @conn.on_message(message_types.MSG_GLOBAL_POSITION)
        def gps_listener(_, name, gps):
            # do whatever with the gps, which will be of type GlobalPosition

        or 

        @conn.on_message('*')
        def all_msg_listener(_, name, msg):
            # this is a listener for all message types, so break out the msg as defined by the name
        """

        def decorator(fn):
            if isinstance(name, list):
                for n in name:
                    self.add_message_listener(n, fn)
            else:
                self.add_message_listener(name, fn)


        return decorator

    def add_message_listener(self, name, fn):

        name = str(name)
        if name not in self._message_listeners:
            self._message_listeners[name] = []
        if fn not in self._message_listeners[name]:
            self._message_listeners[name].append(fn)

    def remove_message_listener(self, name, fn):

        name = str(name)
        if name in self._message_listeners:
            if fn in self._message_listeners[name]:
                self._message_listeners[name].remove(fn)
                if len(self._message_listeners[name]) == 0:
                    del self._message_listeners[name]

    def notify_message_listeners(self, name, msg):

        for fn in self._message_listeners.get(name, []):
            try:
                fn(self, name, msg)
            except Exception as e:
                print("[CONNECTION ERROR] unable to handle message listener")

        for fn in self._message_listeners.get('*', []):
            try:
                fn(self, name, msg)
            except Exception as e:
                print("[CONNECTION ERROR] unable to handle message listener")

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def arm(self):
        pass

    @abstractmethod
    def disarm(self):
        pass

    @abstractmethod
    def take_control(self):
        pass

    @abstractmethod
    def release_control(self):
        pass

    @abstractmethod
    def cmd_attitude(self, yaw, pitch, roll, collective):
        pass

    @abstractmethod
    def cmd_attitude_rate(self, yaw_rate, pitch_rate, roll_rate, collective):
        pass

    @abstractmethod
    def cmd_velocity(self, vn, ve, vd, heading):
        pass

    @abstractmethod
    def cmd_motors(self, motor1, motor2, motor3, motor4):
        pass

    @abstractmethod
    def cmd_position(self, n, e, d, heading):
        pass

    @abstractmethod
    def takeoff(self, n, e, d):
        # mavlink takeoff/land functions need the position for takeoff/land
        # connection class has n knowlege of the vehicle's current position, so drone class needs to send that info
        pass

    @abstractmethod
    def land(self, n, e, d):
        # mavlink takeoff/land functions need the position for takeoff/land
        # connection class has n knowlege of the vehicle's current position, so drone class needs to send that info
        pass

    @abstractmethod
    def set_home_position(self, lat, lon, alt):
        pass
