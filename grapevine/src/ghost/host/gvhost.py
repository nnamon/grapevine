#/usr/bin/python

class Host:
    # Instance Variables
    ip = "127.0.0.1"
    port = 10001
    state =  Host.UNINITIALISED

    # Constants
    UNINITIALISED = 0
    CONNECTED = 1

    def set_state(self, state):
        self.state = state


class HostsController:
    hosts = []
    log_ip = "127.0.0.1"
    log_port = 5000
