import struct
import json

class CraneDataHandler:
    def __init__(self) -> None:
        self.lock_state:bool = 0
        self.unlock_state:bool = 0
        self.landed_state:bool = 0
        self.sprd20ft:bool = 0
        self.sprd40ft:bool = 0
        self.sprd45ft:bool = 0
        self.singleMode:bool = 0
        self.twinMode:bool = 0
        self.trolleyLimit:bool = 0
        self.hoistLimit:bool = 0
        self.flipperSlDown:bool = 0
        self.flipperLlDown:bool = 0
        self.flipperLrDown:bool = 0
        self.flipperSrDown:bool = 0
        self.test_delay_fb:bool = 0
        self.trolleyPos:float = 0
        self.hoistPos:float = 0
        self.loadPosX:float = 0
        self.trolleySpeed:float = 0
        self.hoistSpeed:float = 0
        self.loadSpeedX:float = 0
        self.skewAngle:float = 0
        self.twinGap:float = 0
          
    def parse_data(self, raw_data):

        word1_low = struct.unpack("b",raw_data[0:1])[0]
        word1_high = struct.unpack("b",raw_data[1:2])[0]
        self.lock_state = (word1_low >> 0) & 1
        self.unlock_state = (word1_low >> 1) & 1
        self.landed_state = (word1_low >> 2) & 1
        self.sprd20ft = (word1_low >> 3) & 1
        self.sprd40ft = (word1_low >> 4) & 1
        self.sprd45ft = (word1_low >> 5) & 1
        self.singleMode = (word1_low >> 6) & 1
        self.twinMode = (word1_low >> 7) & 1
        self.trolleyLimit = (word1_high >> 0) & 1
        self.hoistLimit = (word1_high >> 1) & 1
        self.flipperSlDown = (word1_high >> 3) & 1
        self.flipperLlDown = (word1_high >> 4) & 1
        self.flipperLrDown = (word1_high >> 5) & 1
        self.flipperSrDown = (word1_high >> 6) & 1
        self.test_delay_fb = (word1_high >> 7) & 1

        self.trolleyPos = round(float(struct.unpack("i",raw_data[2:6])[0])/1000,3)
        self.hoistPos = round(float(struct.unpack("i",raw_data[6:10])[0])/1000,3)
        self.loadPosX = round(float(struct.unpack("i",raw_data[10:14])[0])/1000,3)
        self.trolleySpeed = round(float(struct.unpack("h",raw_data[14:16])[0])/16384*4.0,3)
        self.hoistSpeed = round(float(struct.unpack("h",raw_data[16:18])[0])/16384*3.0,3)
        self.loadSpeedX = round(float(struct.unpack("h",raw_data[18:20])[0])/1000,3)
        self.skewAngle = round(float(struct.unpack("h",raw_data[20:22])[0])/1000,3)
        self.twinGap = struct.unpack("h",raw_data[22:24])[0]

      
     # 将解析得到的数据转换为json格式并返回
    def data_to_json(self):
        return json.dumps({
            "timestamp": self.timestamp.isoformat(),
            "lock_state": self.lock_state,
            "unlock_state": self.unlock_state,
            "landed_state": self.landed_state,
            "sprd20ft": self.sprd20ft,
            "sprd40ft": self.sprd40ft,
            "sprd45ft": self.sprd45ft,
            "singleMode": self.singleMode,
            "twinMode": self.twinMode,
            "trolleyLimit": self.trolleyLimit,
            "hoistLimit": self.hoistLimit,
            "flipperSlDown": self.flipperSlDown,
            "flipperLlDown": self.flipperLlDown,
            "flipperLrDown": self.flipperLrDown,
            "flipperSrDown": self.flipperSrDown,
            "test_delay_fb": self.test_delay_fb,
            "trolleyPos": self.trolleyPos,
            "hoistPos": self.hoistPos,
            "loadPosX": self.loadPosX,
            "trolleySpeed": self.trolleySpeed,
            "hoistSpeed": self.hoistSpeed,
            "loadSpeedX": self.loadSpeedX,
            "skewAngle": self.skewAngle,
            "twinGap": self.twinGap
        },indent = 4)
