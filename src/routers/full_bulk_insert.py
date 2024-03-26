import csv
import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db_setup.database import SessionLocal, get_db
from ..db_setup import models, schemas
from ..logging_config import configure_api_logging

router = APIRouter()

logger = configure_api_logging('full_bulk_insert')

@router.post('/full-bulk-insert')
def bulk_insert(db: Session = Depends(get_db)):
    batch_size = 1000 
    csv_model_mapping = {
        os.path.join(os.getenv('DATA_DIR', 'data'), 'departments.csv'): (models.Department, schemas.Department, ['id', 'department']),
        os.path.join(os.getenv('DATA_DIR', 'data'), 'jobs.csv'): (models.Job, schemas.Job, ['id', 'job']),
        os.path.join(os.getenv('DATA_DIR', 'data'), 'hired_employees.csv'): (models.HiredEmployee, schemas.HiredEmployee, ['id', 'name', 'datetime', 'department_id', 'job_id']),
    }


    for csv_file, (model, schema, fieldnames) in csv_model_mapping.items():
        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=',', fieldnames=fieldnames)
            objects = []
            for row_number, row in enumerate(csv_reader, start=1):
                try:
                    validated_data = schema(**row)
                    object_data = validated_data.dict()
                    objects.append(model(**object_data))
                    if len(objects) >= batch_size:
                        db.bulk_save_objects(objects)
                        db.commit()
                        objects = []
                except Exception as e:
                    logger.error(f'Non-compliant row in {csv_file} at line {row_number}: {row}')
                    logger.error(f'Error: {str(e)}')
            if objects:
                db.bulk_save_objects(objects)
                db.commit()

    return {'message': 'Data inserted successfully'}