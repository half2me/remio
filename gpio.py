import RPi.GPIO as rio


class Port:
    def __init__(self, app, number, mode='input', default_level=True):
        self.app = app
        self.number = number
        self._mode = None
        self._default = None
        self.mode = mode
        self.default = default_level

    def __del__(self):
        rio.cleanup(self.number)

    @property
    def mode(self):
        return self._mode

    def _onChange(self, channel):
        for _, ws in self.app['websockets'].items():
            ws.send_str('{"port": ' + str(self.number) + '}')

    @mode.setter
    def mode(self, value):
        if value == 'input':
            if self.mode == 'input':
                rio.remove_event_detect(self.number)
            if self.default:
                rio.setup(self.number, rio.IN, pull_up_down=rio.PUD_UP)
            else:
                rio.setup(self.number, rio.IN, pull_up_down=rio.PUD_DOWN)
            self._mode = 'input'
            rio.add_event_detect(self.number, rio.BOTH, self._onChange, bouncetime=50)
        elif value == 'output':
            if self.mode == 'input':
                rio.remove_event_detect(self.number)
            rio.setup(self.number, rio.OUT)
            self._mode = 'output'
            self.level = self._default

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, value):
        self._default = value
        self.mode = self._mode

    @property
    def level(self):
        return rio.input(self.number) == rio.HIGH

    @level.setter
    def level(self, value):
        if self.mode == 'output':
            rio.output(self.number, rio.HIGH) if value else rio.output(self.number, rio.LOW)


class Io:
    def __init__(self):
        print("RPI GPIO version: " + rio.VERSION)
        self._ports = {}

    @property
    def ports(self):
        return self._ports

    async def onStartup(self, app):
        rio.setmode(rio.BCM)  # Broadcom pin-numbering scheme

    async def onShutdown(self, app):
        rio.cleanup()
