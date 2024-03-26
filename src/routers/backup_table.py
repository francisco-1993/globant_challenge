import os
import fastavro
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Integer, Float, DateTime, String
from ..db_setup.database import get_db, Base
from ..logging_config import configure_api_logging

router = APIRouter()

logger = configure_api_logging(api_name='backup_table', append_logs=True)

def get_avro_type(column):

    if isinstance( column.type, Integer):
        return 'int'
    elif isinstance( column.type, Float):
        return 'float'
    elif isinstance(column.type, DateTime):
        return {'type': 'long', 'logicalType': 'timestamp-millis'}
    elif  isinstance(column.type, String):
        return 'string'
    # else:
    #     return 'string'  #default data type


@router.get('/backup-table')
def backup_table(table_name: str, db: Session = Depends(get_db), page_size: int = 1000):
    try:
        # Get the table metadata based on the table name
        table = Base.metadata.tables.get(table_name)
        logger.error(f'Base.metadata.tables.get(table_name) :: {table} ')
        if table is None:
            raise HTTPException(status_code=404, detail=f"Table '{table_name}' does not exist")

        backup_dir = os.getenv('BACKUPS_DIR', 'backups')
        os.makedirs(backup_dir, exist_ok=True)

        backup_file = os.path.join(backup_dir, f'{table_name}.avro')

        logger.error(f'testing :: { [ ( column.name, get_avro_type(column)) for column in table.columns] } ')

        schema = {
            'name': table_name,
            'type': 'record',
            'fields': [{'name': column.name, 'type': get_avro_type(column)} for column in table.columns]
        }

        with open(backup_file, 'wb') as file:
            records = []
            offset = 0
            while True:
                query = db.query(table).offset(offset).limit(page_size)
                chunk_data = query.all()
                if chunk_data:
                    records.extend([dict(zip(table.columns.keys(), row)) for row in chunk_data])
                    offset += page_size
                else:
                    break

            fastavro.writer(file, schema, records)


        return {'message': f"Backup of table '{table_name}' created successfully"}

    except Exception as e:
        logger.error(f'Error creating table backup: {str(e)}')
        raise HTTPException(status_code=500, detail='Error creating table backup')