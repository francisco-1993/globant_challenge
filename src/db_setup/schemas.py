from pydantic import BaseModel, validator
from datetime import datetime

class Department(BaseModel):
    id: int
    department: str

    class config:
        orm_mode = True

class Job(BaseModel):
    id: int
    job: str
    
    class config:
        orm_mode = True

class HiredEmployee(BaseModel):
    id: int
    name: str
    datetime: datetime
    department_id: int
    job_id: int

    @validator('department_id', 'job_id', pre=True)
    def convert_empty_string_to_none(cls, value):
        if value == '':
            return None
        return value

    # @validator('datetime', pre=True)
    # def parse_datetime(cls, value):
    #     return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
    
    class config:
        orm_mode = True

class BatchTransaction(BaseModel):
    departments: list[Department]
    jobs: list[Job]
    hired_employees: list[HiredEmployee]
    
    class config:
        orm_mode = True