#app/services/schedule.py
from typing import List
from schemas.schedule import GenerateScheduleCmd, GenerateScheduleOut
from utilities.schedule_generator import ScheduleGenerator

class ScheduleGenerateUseCase:
    def __init__(self, request_cmd: GenerateScheduleCmd) -> None:
        self.generator = ScheduleGenerator(cmd=request_cmd)
        
    def execute(self) -> List[GenerateScheduleOut]:
        return self.generator.execute()
