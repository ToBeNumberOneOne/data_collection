import struct
import json
import logging

logger = logging.getLogger(__name__)

class CraneDataHandler:
    def __init__(self) -> None:
        logging.info("Initializing CraneDataHandler")
        self.controlOn:bool = 0
        self.autoLandActive:bool = 0
        self.landed:bool = 0
        self.locked:bool = 0
        self.unlocked:bool = 0
        self.sprd20ft:bool = 0
        self.sprd40ft:bool = 0
        self.sprd45ft:bool = 0
        self.microMotorBrakeOn:bool = 0
        self.motorPos1:float = 0
        self.motorPos2:float = 0
        self.motorPos3:float = 0
        self.motorPos4:float = 0
        self.trolleyPos:float = 0
        self.trolleyVel:float = 0
        self.hoistPos:float = 0
        self.hoistVel:float = 0
        self.gantryPos:float = 0
        self.gantryVel:float = 0
        self.faultCodeFb:float = 0
        self.ascFaultCode:float = 0
        self.taskType:float = 0
        self.taskLaneNum:float = 0
        self.workMode:float = 0
        self.taskCntSize:float = 0
        self.taskCntHeight:float = 0
        self.chaissCntType:float = 0

        self.autoLandEnabled:bool = 0
        self.autoLandFailed:bool = 0
        self.autoLandSuccess:bool = 0
        self.landModuleFault:bool = 0
        self.hoistUpCmd:bool = 0
        self.hoistDownCmd:bool = 0
        self.hoistZeroCmd:bool = 0
        self.microMotorBrakeOnCmd:bool = 0
        self.sprdLockCmd:bool = 0
        self.sprdUnlockCmd:bool = 0
        self.microMotor1Ref:float = 0
        self.microMotor2Ref:float = 0
        self.microMotor3Ref:float = 0
        self.microMotor4Ref:float = 0
        self.hoistSpeedRef:float = 0
        self.faultCode:float = 0
        self.camCode:float = 0


          
    def parse_data(self, raw_data):
        #logger.debug("Parsing data: %s", raw_data)

        word1_low = struct.unpack("b",raw_data[0:1])[0]
        word1_high = struct.unpack("b",raw_data[1:2])[0]

        self.controlOn = (word1_low >> 0) & 1
        self.autoLandActive = (word1_low >> 3) & 1
        self.landed = (word1_low >> 4) & 1
        self.locked = (word1_low >> 5) & 1
        self.unlocked = (word1_low >> 6) & 1
        self.sprd20ft= (word1_low >> 7) & 1
        self.sprd40ft = (word1_high >> 0) & 1
        self.sprd45ft = (word1_high >> 1) & 1
        self.microMotorBrakeOn = (word1_high >> 5) & 1
    
        self.motorPos1 = (struct.unpack(">h",raw_data[10:12])[0])
        self.motorPos2 = (struct.unpack(">h",raw_data[12:14])[0])
        self.motorPos3 = (struct.unpack(">h",raw_data[14:16])[0])
        self.motorPos4 = (struct.unpack(">h",raw_data[16:18])[0])

        self.trolleyPos = round(float(struct.unpack(">h",raw_data[18:20])[0])/1000,3)
        self.trolleyVel = round(float(struct.unpack(">h",raw_data[20:22])[0])/1000,3)

        self.hoistPos = round(float(struct.unpack(">h",raw_data[24:26])[0])/1000,3)
        self.hoistVel = round(float(struct.unpack(">h",raw_data[26:28])[0])/1000,3)

        self.gantryPos = round(float(struct.unpack(">i",raw_data[28:32])[0])/1000,3)
        self.gantryVel = round(float(struct.unpack(">h",raw_data[32:34])[0])/1000,3)
        
        self.faultCodeFb = (struct.unpack(">h",raw_data[34:36])[0])
        self.ascFaultCode = (struct.unpack(">h",raw_data[36:38])[0])
        self.taskType = (struct.unpack(">h",raw_data[38:40])[0])
        self.taskLaneNum = (struct.unpack("h",raw_data[40:42])[0])
        self.workMode = (struct.unpack(">h",raw_data[42:44])[0])
        self.taskCntSize = (struct.unpack(">h",raw_data[44:46])[0])
        self.taskCntHeight = (struct.unpack(">h",raw_data[46:48])[0])
        self.chaissCntType = (struct.unpack(">h",raw_data[48:50])[0])

        word26_low = struct.unpack("b",raw_data[50:51])[0]
        word26_high = struct.unpack("b",raw_data[51:52])[0]

        self.autoLandEnabled = (word26_low >> 2) & 1
        self.autoLandFailed = (word26_low >> 3) & 1
        self.autoLandSuccess = (word26_low >> 4) & 1
        self.landModuleFault = (word26_low >> 5) & 1
        self.hoistUpCmd = (word26_low >> 7) & 1
        self.hoistDownCmd = (word26_high >> 0) & 1
        self.hoistZeroCmd = (word26_high >> 1) & 1
        self.microMotorBrakeOnCmd = (word26_high >> 2) & 1
        self.sprdLockCmd = (word26_high >> 3) >> 1
        self.sprdUnlockCmd = (word26_high >> 4) >> 0

        self.microMotor1Ref = (struct.unpack(">h",raw_data[52:54])[0])*21/16384
        self.microMotor2Ref = (struct.unpack(">h",raw_data[54:56])[0])*21/16384
        self.microMotor3Ref = (struct.unpack(">h",raw_data[56:58])[0])*21/16384
        self.microMotor4Ref = (struct.unpack(">h",raw_data[58:60])[0])*21/16384
        self.hoistSpeedRef = round(float(struct.unpack(">h",raw_data[62:64])[0])/255*1.0,3)
        self.faultCode = (struct.unpack(">h",raw_data[64:66])[0])
        self.camCode = (struct.unpack(">h",raw_data[66:68])[0])

        