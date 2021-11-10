from datetime import datetime
from enum import Enum

from domain.note.exceptions import NoteNotFoundException
from domain.note.model import Note
from domain.note.storage import NoteStorageI

notes_data = {
    '1': Note(id=1, header="header1", text="text1", tags=["a1", "b1", "c1"], author="me1", likes=1, comments=1, color=1,
              created_date=datetime.strftime(datetime.utcnow(), "%s"),
              modified_date=datetime.strftime(datetime.utcnow(), "%s")),
    '2': Note(id=2, header="header2", text="text2", tags=["a2", "b2", "c2"], author="me2", likes=2, comments=2, color=2,
              created_date=datetime.strftime(datetime.utcnow(), "%s"),
              modified_date=datetime.strftime(datetime.utcnow(), "%s")),
    '3': Note(id=3, header="header3", text="text3", tags=["a3", "b3", "c3"], author="me3", likes=3, comments=3, color=3,
              created_date=datetime.strftime(datetime.utcnow(), "%s"),
              modified_date=datetime.strftime(datetime.utcnow(), "%s")),
    '4': Note(id=4, header="header4", text="text4", tags=["a4", "b4", "c4"], author="me4", likes=4, comments=4, color=4,
              created_date=datetime.strftime(datetime.utcnow(), "%s"),
              modified_date=datetime.strftime(datetime.utcnow(), "%s")),
    '5': Note(id=5, header="header5", text="text5", tags=["a5", "b5", "c5"], author="me5", likes=5, comments=5, color=5,
              created_date=datetime.strftime(datetime.utcnow(), "%s"),
              modified_date=datetime.strftime(datetime.utcnow(), "%s")),
}


class NoteStorage(NoteStorageI):

    def create(self, note: Note):
        new_note_id = len(notes_data.keys()) + 1
        notes_data[str(new_note_id)] = note
        note.id = new_note_id
        return note

    def update(self, note: Note):
        if str(note.id) not in notes_data.keys():
            raise NoteNotFoundException(message="note not found")
        notes_data.update({str(note.id): note})
        return note

    def delete(self, note_id: int):
        try:
            notes_data.pop(str(note_id))
        except KeyError as e:
            raise NoteNotFoundException(message="note not found")

    def get_one(self, note_id: str):
        try:
            return notes_data[str(note_id)]
        except KeyError as e:
            raise NoteNotFoundException(message="note not found")

    def get_all(self, limit: int, offset: int):
        notes = list(notes_data.values())[offset:limit + offset]
        return notes
