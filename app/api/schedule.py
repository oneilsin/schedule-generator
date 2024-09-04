from fastapi import APIRouter, HTTPException, Body
from typing import List
from schemas.schedule import GenerateScheduleCmd, GenerateScheduleOut
from services.schedule import ScheduleGenerateUseCase

router = APIRouter()

@router.post("/generate_schedule", response_model=List[GenerateScheduleOut])
async def generate_schedule(
    generate_schedule_body_in: GenerateScheduleCmd = Body(..., description="Schedule fields to create")
) -> List[GenerateScheduleOut]:
    try:
        generator = ScheduleGenerateUseCase(generate_schedule_body_in)
        result = generator.execute()
        if result is None or not isinstance(result, list):
            raise HTTPException(status_code=500, detail="Internal Server Error: Invalid response format")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
