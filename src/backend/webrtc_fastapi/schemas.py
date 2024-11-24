from pydantic import BaseModel


class OfferSchema(BaseModel):
    sdp: str
    type: str
    name: str
