from abc import ABC, abstractmethod

from domain.note.dto import *
from domain.note.model import Note


class NoteServiceI(ABC):
    @abstractmethod
    def get_notes(self, filters: dict, limit: int, offset: int) -> List[Note]: pass

    @abstractmethod
    def get_note(self, note_id) -> Note: pass

    @abstractmethod
    def create_note(self, note: CreateNoteDTO) -> Note: pass

    @abstractmethod
    def delete_note(self, note_id): pass

    @abstractmethod
    def update_note(self, note: UpdateNoteDTO): pass

    @abstractmethod
    def partially_update(self, note: PartiallyUpdateNoteDTO): pass
