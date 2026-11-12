#app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///./app.db" #define database connection.  app.db (data file nane)

engine = create_engine(   #creates a SQLAlchemy engine. connection point to communicate with the database
    DATABASE_URL, 
    connect_args={"check_same_thread": False} #disables this restrictions so multiple requests handlers can use the same database connection.
)

#generates customized Session clases with predefines seetings. Autocommit disables committing of transactions
#autoflush, prevents SQLAlchemy from automatically sending pending in memory object changes to database before query
#bind links this session factory directly to the engine created.
SessionLocal = sessionmaker(autocommit = False, autoflush =False, bind =engine)

class Base(DeclarativeBase): #defines the base class from which all the database models (tables) will inherit
    pass 

#generator function designed to be used as a dependency to give each incoming http requeat its own database session
def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()

