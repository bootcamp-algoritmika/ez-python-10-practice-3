from wsgiref import simple_server

import falcon
from falcon import App

from adapters.api.controllers import NotesResource, NoteResource
from adapters.db.note.storage import NoteStorage
from domain.note.service import NoteService

storage = NoteStorage()
service = NoteService(storage=storage)


def create_app() -> App:
    app = falcon.App()

    notes_view = NotesResource(service=service)
    note_view = NoteResource(service=service)

    app.add_route('/notes/', notes_view)
    app.add_route('/notes/{note_id}', note_view)
    return app


app = create_app()
httpd = simple_server.make_server('127.0.0.1', 1234, app)
httpd.serve_forever()
