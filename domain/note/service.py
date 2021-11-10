from datetime import datetime
from typing import List

from adapters.interfaces import NoteServiceI
from domain.note.dto import CreateNoteDTO, UpdateNoteDTO, PartiallyUpdateNoteDTO
from domain.note.model import Note
from domain.note.storage import NoteStorageI


class NoteService(NoteServiceI):
    def __init__(self, storage: NoteStorageI):
        self.storage = storage

    def get_notes(self, filters: dict, limit: int, offset: int) -> List[Note]:
        notes = self.storage.get_all(limit, offset)
        # вообще фильтрация через сторадж, но для наглядности бизнес логики и слоя - вынес сюда
        if len(filters.values()) > 0:
            notes = self.filter_data(filters=filters, notes=notes)
        return notes

    def get_note(self, note_id) -> Note:
        notes = self.storage.get_one(note_id=note_id)
        return notes

    def create_note(self, note: CreateNoteDTO) -> Note:
        note = Note(**note.__dict__, created_date=datetime.strftime(datetime.utcnow(), "%s"))
        return self.storage.create(note=note)

    def delete_note(self, note_id) -> None:
        self.storage.delete(note_id=note_id)

    def update_note(self, note: UpdateNoteDTO):
        note = Note(**note.__dict__)
        note.modified_date = datetime.strftime(datetime.utcnow(), "%s")
        self.storage.update(note=note)

    def partially_update(self, note: PartiallyUpdateNoteDTO):
        old_note = self.get_note(note.id)
        if note.header is not None:
            old_note.header = note.header
        if note.text is not None:
            old_note.text = note.text
        if note.tags is not None and len(note.tags) > 0:
            old_note.tags = note.tags
        if note.author is not None:
            old_note.author = note.author
        if note.likes is not None:
            old_note.likes = note.likes
        if note.comments is not None:
            old_note.comments = note.comments
        if note.color is not None:
            old_note.color = note.color

        old_note.modified_date = datetime.strftime(datetime.utcnow(), "%s")
        self.storage.update(note=old_note)

    def filter_data(self, filters, notes) -> list:
        header_filter = filters.get("header")
        tags_filter = filters.get("tags")
        likes_filter = filters.get("likes")
        comments_filter = filters.get("comments")
        result = []
        for d in notes:
            if header_filter is not None:
                op = header_filter.split(":")[0]
                val = header_filter.split(":")[1]
                header = d.header
                if op == "like":
                    if val in header:
                        result.append(d)
                elif op == "eq":
                    if val == header:
                        result.append(d)
            if tags_filter is not None:
                # only IN operator available
                val = tags_filter.split(":")[1]
                if len(list(set(val.split(",")) & set(d.tags))) > 0:
                    result.append(d)
            if likes_filter is not None:
                op = likes_filter.split(":")[0]
                val = likes_filter.split(":")[1]
                likes = d.likes
                to_append = self.compare_ops(op, t_val=val, s_val=likes)
                if to_append:
                    result.append(d)
            if comments_filter is not None:
                op = comments_filter.split(":")[0]
                val = comments_filter.split(":")[1]
                comments = d.comments
                to_append = self.compare_ops(op, t_val=val, s_val=comments)
                if to_append:
                    result.append(d)
        return result

    def compare_ops(self, op, t_val, s_val) -> bool:
        if op == "gt":
            if s_val > int(t_val):
                return True
        elif op == "gte":
            if s_val >= int(t_val):
                return True
        elif op == "lt":
            if s_val < int(t_val):
                return True
        elif op == "lte":
            if s_val <= int(t_val):
                return True
        elif op == "eq":
            if s_val == int(t_val):
                return True

        return False
