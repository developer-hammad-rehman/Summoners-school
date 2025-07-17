from bson import ObjectId

from ..exceptions.base_exceptions import BadRequest


def isvalidate_id(id:str):
    if not ObjectId.is_valid(id):
            raise BadRequest("Invalid  ID Format")