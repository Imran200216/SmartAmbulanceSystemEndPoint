from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class AmbulanceStatusRecord(BaseModel):
    employeeEmail: Optional[str]
    employeeId: Optional[str]
    hospitalAddress: Optional[str]
    hospitalName: Optional[str]
    isAmbulanceDriverSelectedHospital: Optional[bool]
    timestamp: Optional[datetime]
