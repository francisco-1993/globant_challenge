from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db_setup import models, schemas
from ..db_setup.database import get_db
from ..logging_config import configure_api_logging

router = APIRouter()

logger = configure_api_logging('batch_transactions')

@router.post('/batch-transactions')
def batch_transactions(batch: schemas.BatchTransaction, db: Session = Depends(get_db)):
    
    if (len(batch.departments) + len(batch.jobs) + len(batch.hired_employees)) > 1000:
        raise HTTPException(status_code=400, detail='Batch size exceeds the limit of 1000 rows in total')

    department_objects = []
    job_objects = []
    employee_objects = []

    for department in batch.departments:
        try:
            department_objects.append(models.Department(**department.model_dump()))
        except Exception as e:
            logger.error(f'Non-compliant department: {department.model_dump_json()}. Error: {str(e)}')

    for job in batch.jobs:
        try:
            job_objects.append(models.Job(**job.model_dump()))
        except Exception as e:
            logger.error(f'Non-compliant job: {job.model_dump_json()}. Error: {str(e)}')

    for employee in batch.hired_employees:
        try:
            employee_objects.append(models.HiredEmployee(**employee.model_dump()))
        except Exception as e:
            logger.error(f'Non-compliant hired employee: {employee.model_dump_json()}. Error: {str(e)}')

    try:
        db.bulk_save_objects(department_objects + job_objects + employee_objects)
        db.commit()
        return {'message': 'Batch transactions inserted successfully'}
    except Exception as e:
        db.rollback()
        logger.error(f'Error inserting batch transactions: {str(e)}')
        raise HTTPException(status_code=400, detail='Error inserting batch transactions')