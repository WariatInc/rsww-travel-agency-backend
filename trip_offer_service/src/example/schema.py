import marshmallow as ma


class ExampleUpsertSchema(ma.Schema):
    class Meta:
        unknown = ma.EXCLUDE

    title = ma.fields.String(required=False)
    author = ma.fields.String(required=False)
