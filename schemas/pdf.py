from pydantic import BaseModel


class DataReportCreate(BaseModel):
    patient_id: int
    professional_user_id: int
