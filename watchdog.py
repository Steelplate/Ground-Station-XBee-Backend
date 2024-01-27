from threading import Timer

class Watchdog(Exception):
    def __init__(self, timeout, userHandler):  # timeout in seconds
        self.timeout = timeout
        self.timer = Timer(self.timeout, self.handler)
        self.timer.start()
        self.userHandler = userHandler

    def reset(self):
        self.timer.cancel()
        self.timer = Timer(self.timeout, self.handler)
        self.timer.start()

    def stop(self):
        self.timer.cancel()

    def handler(self):
        self.userHandler()
        self.reset()