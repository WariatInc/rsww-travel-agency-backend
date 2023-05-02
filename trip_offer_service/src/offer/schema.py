from uuid import UUID
from marshmallow import *


class OfferSchema(Schema):
    uuid: UUID

