import RPi.GPIO as rio


class Port:
    def __init__(self, number, mode='in'):
        self.number = number
        self._mode = None
        self.mode = mode

    @property
    def mode(self):
        return self._mode

    def _onChange(self, channel):
        print("PORT " + str(self.number) + " STATUS: " + str(self.level))

    @mode.setter
    def mode(self, value):
        if value == 'in':
            if self.mode == 'in':
                rio.remove_event_detect(self.number)
            rio.setup(self.number, rio.IN, pull_up_down=rio.PUD_UP)
            self._mode = 'in'
            rio.add_event_detect(self.number, rio.BOTH, self._onChange, bouncetime=50)
        elif value == 'out':
            if self.mode == 'in':
                rio.remove_event_detect(self.number)
            rio.setup(self.number, rio.OUT)
            self._mode = 'out'

    @property
    def level(self):
        return rio.input(self.number)

    @level.setter
    def level(self, value):
        if value == 0:
            rio.output(self.number, rio.LOW)
        elif value == 1:
            rio.output(self.number, rio.HIGH)


class Io:
    def __init__(self):
        print("RPI GPIO version: " + rio.VERSION)
        self._ports = {}

    @property
    def ports(self):
        return self._ports

    async def onStartup(self, app):
        rio.setmode(rio.BCM)  # Broadcom pin-numbering scheme
        self.ports[23] = Port(23, 'out')
        self.ports[23].level = 0

        self.ports[18] = Port(18, 'in')

    async def onShutdown(self, app):
        rio.cleanup()
