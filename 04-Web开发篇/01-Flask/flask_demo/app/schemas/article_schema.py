"""文章Schema"""

from marshmallow import Schema, fields


class ArticleSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str()
    status = fields.Str(load_default="draft")
    author_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
