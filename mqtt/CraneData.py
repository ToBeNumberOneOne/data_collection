
class CraneData:
    def __init__(self) -> None:
        self.lock_state = 0
        self.unlock_state = 0
        self.landed_state = 0
        self._20ft = 0
        self._40ft = 0
        self._45ft = 0
        self.singleMode = 0
        self.twinMode = 0
        self.trolleyLimit = 0
        self.hoistLimit = 0
        self.flipperSlDown = 0
        self.flipperLlDown = 0
        self.flipperLrDown = 0
        self.flipperSrDown = 0
        self.test_delay_fb = 0
        self.trolleyPos = 0
        self.hoistPos = 0
        self.loadPosX = 0
        self.trolleySpeed = 0
        self.hoistSpeed = 0
        self.loadSpeedX = 0
        self.skewAngle = 0
        self.twinGap = 0

