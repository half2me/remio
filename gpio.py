import RPi.GPIO as rio


class Port:
    def __init__(self, number, mode='in', default=1):
        self.number = number
        self._mode = None
        self._default = None
        self.mode = mode
        self.default = default

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
            if self.default == 1:
                rio.setup(self.number, rio.IN, pull_up_down=rio.PUD_UP)
            else:
                rio.setup(self.number, rio.IN, pull_up_down=rio.PUD_DOWN)
            self._mode = 'in'
            rio.add_event_detect(self.number, rio.BOTH, self._onChange, bouncetime=50)
        elif value == 'out':
            if self.mode == 'in':
                rio.remove_event_detect(self.number)
            rio.setup(self.number, rio.OUT)
            self._mode = 'out'
            self.level = 1

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, value):
        self._default = value
        self.mode = self._mode

    @property
    def level(self):
        return 1 if rio.input(self.number) == rio.HIGH else 0

    @level.setter
    def level(self, value):
        rio.output(self.number, rio.HIGH) if value == 1 else rio.output(self.number, rio.LOW)


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
