from enum import Enum

class Stage(str,Enum):
    OBSERVE="observe"
    DETECT_LOG="detect_log"
    CONTROLLED_MITIGATION="controlled_mitigation"
    ROLLBACK="rollback"

class Policy:
    def __init__(self,threshold:float,allow_mitigation:bool=False):
        self.threshold=threshold
        self.allow_mitigation=allow_mitigation
        self.stage=Stage.OBSERVE
        self.history=[]

    def evaluate(self,score:float,resource_id:str):
        if score < self.threshold:
            self.stage=Stage.OBSERVE
            self.history.append({"stage":self.stage.value,"score":score,"resource":resource_id})
            return self.stage
        self.stage=Stage.DETECT_LOG
        self.history.append({"stage":self.stage.value,"score":score,"resource":resource_id})
        return self.stage

    def request_mitigation(self,resource_id:str):
        if not self.allow_mitigation:
            self.history.append({"stage":self.stage.value,"action":"mitigation_blocked_safe_default","resource":resource_id})
            return False
        if self.stage != Stage.DETECT_LOG:
            return False
        self.stage=Stage.CONTROLLED_MITIGATION
        self.history.append({"stage":self.stage.value,"resource":resource_id})
        return True

    def rollback(self,resource_id:str):
        self.stage=Stage.ROLLBACK
        self.history.append({"stage":self.stage.value,"resource":resource_id})
        self.stage=Stage.OBSERVE
        self.history.append({"stage":self.stage.value,"resource":resource_id,"recovered":True})
