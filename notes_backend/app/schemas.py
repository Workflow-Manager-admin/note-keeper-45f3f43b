from marshmallow import Schema, fields, validate

# PUBLIC_INTERFACE
class NoteSchema(Schema):
    """Schema for serializing/deserializing Note objects."""
    id = fields.Str(dump_only=True, description="Unique ID of the note")
    title = fields.Str(required=True, description="Title of the note", validate=validate.Length(min=1))
    content = fields.Str(required=True, description="Content of the note", validate=validate.Length(min=1))
    timestamp = fields.Str(dump_only=True, description="Timestamp of when the note was created or updated")

# For partial updates (PATCH)
# PUBLIC_INTERFACE
class NoteUpdateSchema(Schema):
    title = fields.Str(required=False, description="Title of the note", validate=validate.Length(min=1))
    content = fields.Str(required=False, description="Content of the note", validate=validate.Length(min=1))
