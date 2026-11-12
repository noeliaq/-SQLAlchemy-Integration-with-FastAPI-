#app/main.py
from fastapi import FastAPI
from app.database import engine, Base
from app.models import notes as notes_model  #Import so Base registers the model
from app.routers import notes 

#Create Tables
Base.metadata.create_all(bind = engine)

app = FastAPI(title= "Database-Backend Notes API")
app.include_router(notes.router)