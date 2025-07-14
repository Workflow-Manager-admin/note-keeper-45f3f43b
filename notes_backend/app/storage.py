import os
import json
from threading import Lock
from .models import Note

NOTES_FILE = os.getenv("NOTES_FILE_PATH", "notes_data.json")

# Thread-safe storage for process memory
_notes = {}
_lock = Lock()

def _load_from_file():
    """Load notes from file, used on startup."""
    global _notes
    if not os.path.exists(NOTES_FILE):
        _notes = {}
        return
    with open(NOTES_FILE, "r") as f:
        try:
            data = json.load(f)
            _notes = {note["id"]: Note.from_dict(note) for note in data}
        except Exception:
            _notes = {}

def _save_to_file():
    """Persist all notes to file."""
    with open(NOTES_FILE, "w") as f:
        notes_list = [note.to_dict() for note in _notes.values()]
        json.dump(notes_list, f)

# PUBLIC_INTERFACE
def get_all_notes():
    """Return all notes as a list of Note objects."""
    with _lock:
        return list(_notes.values())

# PUBLIC_INTERFACE
def get_note(note_id):
    """Retrieve a single Note by its id."""
    with _lock:
        return _notes.get(note_id)

# PUBLIC_INTERFACE
def add_note(note: Note):
    """Add a new note and persist to file."""
    with _lock:
        _notes[note.id] = note
        _save_to_file()
        return note

# PUBLIC_INTERFACE
def update_note(note_id, title=None, content=None):
    """Update the title/content of a note."""
    with _lock:
        note = _notes.get(note_id)
        if not note:
            return None
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        _save_to_file()
        return note

# PUBLIC_INTERFACE
def delete_note(note_id):
    """Delete a note by id."""
    with _lock:
        note = _notes.pop(note_id, None)
        _save_to_file()
        return note

# On import, always load data
_load_from_file()
