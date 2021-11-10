from abc import ABC, abstractmethod

from domain.note.model import Note


class NoteStorageI(ABC):

    @abstractmethod
    def get_one(self, note_id: int):
        pass

    @abstractmethod
    def get_all(self, limit: int, offset: int):
        pass

    @abstractmethod
    def create(self, note: Note):
        pass

    @abstractmethod
    def update(self, note: Note):
        pass

    @abstractmethod
    def delete(self, note_id: int):
        pass
