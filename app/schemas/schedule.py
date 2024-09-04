#app/schemas/schedule.py
from dataclasses import dataclass
from decimal import Decimal
from datetime import date
from pydantic import BaseModel
from common.enums import ScheduleStatus

class GenerateScheduleCmd(BaseModel):
    requested_amount: Decimal
    annual_effective_rate: Decimal
    installment_number: int
    disbursement_date: date
    start_date: date
    
class GenerateScheduleOut(BaseModel):
    due_date: date = date.today()
    days_difference: int = 0
    installment_number: int = 0
    principal_amount: Decimal = Decimal(0)
    principal_amortization_amount: Decimal = Decimal(0)
    interest_amount: Decimal = Decimal(0)
    installment_amount_without_tax: Decimal = Decimal(0)
    tax_amount: Decimal = Decimal(0)
    installment_amount_with_tax: Decimal = Decimal(0)
    comments: str = "Initial disbursement"
    schedule_status: ScheduleStatus = ScheduleStatus.PENDING