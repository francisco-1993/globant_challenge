import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import text
from ..db_setup.database import get_db, engine
from fastavro import reader
from ..logging_config import configure_api_logging

router = APIRouter()
logger = configure_api_logging(api_name='restore_table', append_logs=True)

@router.post('/restore-table')
def restore_table(table_name: str, db: Session = Depends(get_db), ):
    try:
        backup_dir = os.getenv('BACKUPS_DIR', 'backups')
        backup_file = os.path.join(backup_dir, f'{table_name}.avro')

        if not os.path.exists(backup_file):
            raise HTTPException(status_code=404, detail=f"Backup file for table '{table_name}' does not exist")

        delete_query = text(f"DELETE FROM {table_name} WHERE TRUE")
        db.execute(delete_query)
        db.commit()

        # Separate session for bulk operations
        # BulkSession = sessionmaker(bind=engine)
        # bulk_session = BulkSession()

        #try:
        with open(backup_file, 'rb') as file:
            avro_reader = reader(file)
            schema = avro_reader.schema
            columns = [field['name'] for field in schema['fields']]

            # Read the Avro records in batches
            batch_size = 1000
            batch = []

            for record in avro_reader:
                batch.append(dict(zip(columns, record)))

                if len(batch) >= batch_size:
                    db.bulk_insert_mappings(table_name, batch)
                    db.commit()
                    batch = []

            if batch:
                db.bulk_insert_mappings(table_name, batch)
                db.commit()

        # finally:
        #     bulk_session.close()

        return {'message': f"Table '{table_name}' restored successfully"}

    except Exception as e:
        logger.error(f'Error restoring table: {str(e)}')
        raise HTTPException(status_code=500, detail='Error restoring table')