#app/routers/notes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.notes import Note
from app.schemas.notes import NoteCreate, NoteResponse

router = APIRouter(prefix = "/notes", tags = ["Notes"]) #creates an APIRouter instance in FastAPI to organize, group, and modularize endpoints

@router.post("/", response_model = NoteResponse, status_code=201)
#tells FastAPI to seu the Note response schema to validate seralize and filter the outgoing dat before sending it back to the client
def create_note(
    note:NoteCreate, 
    db:Session = Depends(get_db)):
    #db:Session=Depends(get_db) tells FastAPI to automatically inject a database session into the function when a request arrives

    """Create a new note in the database """
    db_note = Note(
        title = note.title,
        content = note.content,
        category = note.category,
        is_pinned = note.is_pinned
    )
    #To unpack the schema we can use .model_dump()instead of typing all fields manually. 

    db.add(db_note)             #Stage a new record
    db.commit()                 #Saves to the database
    db.refresh(db_note)         #Reload to get the autogenereated id and created at
    return db_note              #Pydantic converts vai from attributes

@router.get("/", response_model=list[NoteResponse])

def list_notes(
    category: Optional[str] = None,
    is_pinned: Optional[bool] = None,
    db:Session = Depends(get_db)
):

    """List notes with optional category and optional is_pinned """

    query = db.query(Note)
    if category :
        query = query.filter(Note.category == category)
    if is_pinned is not None:
        query = query.filter(Note.is_pinned == is_pinned)

    notes = query.order_by(Note.is_pinned.desc(), Note.created_at.desc()).all()
    return notes

@router.get("/{note_id}", response_model= NoteResponse)

def get_note (
    note_id: int, 
    db:Session = Depends(get_db)
):
    """Get specific Note by Id"""
    note = db.query(Note).filter(Note.id== note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail= "Note ID not found")

    return note


@router.delete("/{note_id}", response_model=NoteResponse)

def delete_note(
    note_id : int,
    db:Session = Depends(get_db)
):
    """Delete a specific Note by Id"""

    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail = "Note ID not found")
 
    db.delete (note)
    db.commit ()

    return note


