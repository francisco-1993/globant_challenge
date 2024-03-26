from fastapi import FastAPI
from .db_setup.database import engine
from .db_setup import models
from .routers import full_bulk_insert, batch_transactions, backup_table, restore_table

app = FastAPI()

# creation of the actual tables acording to the tables and constrains defined in models
models.Base.metadata.create_all(bind=engine)

app.include_router(full_bulk_insert.router)
app.include_router(batch_transactions.router)
app.include_router(backup_table.router)
app.include_router(restore_table.router)

# @app.get("/")
# def root():
#     return {'message': 'API running'}