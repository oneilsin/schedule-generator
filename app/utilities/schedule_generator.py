#app/schemas/schedule_generator.py
from decimal import Decimal, getcontext
from typing import List
from schemas.schedule import GenerateScheduleCmd, GenerateScheduleOut
from dateutil.relativedelta import relativedelta
from common.enums import ScheduleStatus


class ScheduleGenerator:
    def __init__(self, cmd:GenerateScheduleCmd) -> None:
        self.cmd = cmd
        getcontext().prec = 10
        
    def pmt(self, interest_rate, loan_amount, number_of_periods):
        # PMT calculation for loan payment
        if interest_rate == 0:
            return loan_amount / number_of_periods
        return loan_amount * (interest_rate * (1 + interest_rate) ** number_of_periods) / ((1 + interest_rate) ** number_of_periods - 1)

    def execute(self) -> List[GenerateScheduleOut]:
        schedule = []
        
        # Inputs
        monthly_effective_rate = (Decimal(1) + self.cmd.annual_effective_rate) ** (Decimal(1) / Decimal(12)) - Decimal(1)
        daily_effective_rate = (Decimal(1) + monthly_effective_rate) ** (Decimal(1) / Decimal(30)) - Decimal(1)
        base_amount = self.cmd.requested_amount
        principal_balance = base_amount
        total_installment = self.cmd.installment_number
        due_date = self.cmd.start_date
        disbursement_date = self.cmd.disbursement_date
        base_installment_amount = self.pmt(
            interest_rate=monthly_effective_rate,
            loan_amount=principal_balance,
            number_of_periods=total_installment
        )        
        tax_rate = Decimal(0.18)        
        schedule.append(
            GenerateScheduleOut(
                    due_date=disbursement_date,
                    principal_amount=principal_balance,
                    principal_amortization_amount=0,
                    interest_amount=0,
                    installment_amount_without_tax=0,
                    tax_amount=0,
                    installment_amount_with_tax=0,
                    comments=f"Installment no. {0}",
                    schedule_status=ScheduleStatus.PENDING
                )
        )
        
        days_difference = (due_date - disbursement_date).days
        amortization = base_installment_amount - (monthly_effective_rate*principal_balance)
        
        for installment_number in range(1, total_installment + 1):
            previous_due_date = due_date
            previous_principal_balance = principal_balance

            
            if installment_number == 1:
                interest_amount = base_amount * daily_effective_rate * Decimal(days_difference)    
                principal_amortization = previous_principal_balance if principal_balance <= 0 else amortization
                installment_amount_without_tax = principal_amortization + interest_amount
            else:
                installment_amount_without_tax = base_installment_amount
                interest_amount = previous_principal_balance * monthly_effective_rate
                amortization = 0 if (installment_amount_without_tax-interest_amount > base_amount) else (+installment_amount_without_tax-interest_amount)
            
            principal_amortization = previous_principal_balance if principal_balance <= 0 else amortization
            principal_balance = max(0, previous_principal_balance - amortization)
             
            tax_amount = tax_rate * interest_amount   
            installment_amount_with_tax = tax_amount + installment_amount_without_tax
            
            schedule.append(
                GenerateScheduleOut(
                    due_date=due_date,
                    days_difference=days_difference,
                    installment_number=installment_number,
                    principal_amount=round(principal_balance,4),
                    principal_amortization_amount=round(principal_amortization,4),
                    interest_amount=round(interest_amount,4),
                    installment_amount_without_tax=round(installment_amount_without_tax,4),
                    tax_amount=round(tax_amount,4),
                    installment_amount_with_tax=round(installment_amount_with_tax,4),
                    comments=f"Installment no. {installment_number}",
                    schedule_status=ScheduleStatus.PENDING
                )
            )
            
            # Move to the next due date (the same day of the next month)
            due_date += relativedelta(months=1)
            days_difference = (due_date - previous_due_date).days
        
        return schedule
                
                