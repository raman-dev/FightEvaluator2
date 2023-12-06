from fastapi import APIRouter,Depends
from datetime import datetime
from sqlmodel import Session
from dependencies import get_session
from models import Note,NoteIn


router = APIRouter(
    tags=["notes"],
)

@router.get("/notes/{assessment_id}")
async def get_notes(assessment_id: int,session: Session = Depends(get_session)):
    #get notes for assessment id with session
    notes = None
    notes = session.query(Note).filter(Note.assessment_id == assessment_id).all()
    return notes

@router.post("/notes/create-note")
async def create_note(noteIn: NoteIn,session: Session = Depends(get_session)):#,request: Request):
    #add note to database
    # body = await request.body()
    # print('\nRECEIVED FROM BROWSER\n',body,noteIn.data)
    note = Note(assessment_id=noteIn.assessment_id,data=noteIn.data,timestamp=datetime.now().isoformat())
    session.add(note)
    session.commit()
    session.refresh(note)
    return note

@router.delete("/notes/delete-note/{note_id}")
async def delete_notes(note_id,session: Session = Depends(get_session)):
    #delete note from database
    note = session.get(Note,note_id)
    if not note:
        return {'status':'failed'}
    session.delete(note)
    session.commit()
    return {'status':'success'}

#add all note delete by assessment id
@router.delete("/notes/delete-note/assessment/{assessment_id}")
async def delete_notes_by_assessment(assessment_id,session: Session = Depends(get_session)):
    #delete note from database
    notes = session.query(Note).filter(Note.assessment_id == assessment_id).all()
    if not notes:
        return {'status':'failed'}
    for note in notes:
        session.delete(note)
    session.commit()
    return {'status':'success'}
