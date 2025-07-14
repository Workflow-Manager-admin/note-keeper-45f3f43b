from flask_smorest import Blueprint, abort
from flask.views import MethodView

from ..models import Note
from ..schemas import NoteSchema, NoteUpdateSchema
from .. import storage

blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/notes",
    description="Endpoints for managing notes (CRUD)"
)

@blp.route("/")
class NotesList(MethodView):
    """Handles listing and creation of notes."""

    # PUBLIC_INTERFACE
    @blp.response(200, NoteSchema(many=True))
    def get(self):
        """Get all notes."""
        return [note.to_dict() for note in storage.get_all_notes()]

    # PUBLIC_INTERFACE
    @blp.arguments(NoteSchema)
    @blp.response(201, NoteSchema)
    def post(self, new_note_data):
        """Create a new note."""
        note = Note(title=new_note_data["title"], content=new_note_data["content"])
        storage.add_note(note)
        return note.to_dict()

@blp.route("/<string:note_id>")
class NoteDetail(MethodView):
    """Handles get, update, and delete for a specific note."""

    # PUBLIC_INTERFACE
    @blp.response(200, NoteSchema)
    def get(self, note_id):
        """Get a specific note by its ID."""
        note = storage.get_note(note_id)
        if not note:
            abort(404, message="Note not found")
        return note.to_dict()

    # PUBLIC_INTERFACE
    @blp.arguments(NoteUpdateSchema)
    @blp.response(200, NoteSchema)
    def patch(self, patch_data, note_id):
        """Update an existing note (one or more fields)."""
        note = storage.get_note(note_id)
        if not note:
            abort(404, message="Note not found")
        updated_note = storage.update_note(note_id, **patch_data)
        return updated_note.to_dict()

    # PUBLIC_INTERFACE
    @blp.response(204)
    def delete(self, note_id):
        """Delete a note by ID."""
        note = storage.delete_note(note_id)
        if not note:
            abort(404, message="Note not found")
        return "", 204
