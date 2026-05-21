from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import Note
from schemas import NoteCreate
from ai import summarize_text

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB Connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "AI Notes App Running"}

# Create Note
@app.post("/notes")
def create_note(note: NoteCreate, db: Session = Depends(get_db)):

    summary = summarize_text(note.content)

    new_note = Note(
        title=note.title,
        content=note.content,
        summary=summary
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note

# Get Notes
@app.get("/notes")
def get_notes(db: Session = Depends(get_db)):
    return db.query(Note).all()

# Update Note
@app.put("/notes/{note_id}")
def update_note(note_id: int, note: NoteCreate, db: Session = Depends(get_db)):

    existing_note = db.query(Note).filter(Note.id == note_id).first()

    existing_note.title = note.title
    existing_note.content = note.content

    # Re-summarize
    existing_note.summary = summarize_text(note.content)

    db.commit()

    return existing_note
@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):

    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        return {"message": "Note not found"}

    db.delete(note)

    db.commit()

    return {"message": "Note deleted successfully"}