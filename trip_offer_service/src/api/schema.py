from marshmallow import missing

non_nullable = dict(required=True, allow_none=False)
explicitly_nullable = dict(required=True, allow_none=True)
implicitly_nullable = dict(
    required=False, allow_none=True, load_default=None, dump_default=None
)
possibly_undefined_nullable = dict(
    required=False, allow_none=True, load_default=missing, dump_default=missing
)
possibly_undefined_non_nullable = dict(
    required=False,
    allow_none=False,
    load_default=missing,
    dump_default=missing,
)
