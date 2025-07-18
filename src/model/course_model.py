from bson import ObjectId
from pydantic import BaseModel, Field , ConfigDict, validator
from typing import Literal, Optional 
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class Owner(BaseModel):
    id : int
    name:str

class CourseModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    rating: float 
    owner : Owner
    view : int
    price:float
    type : Literal["recommended" , "popular" , "new" ,"nothing"]

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Demo",
                "description": "Demo",
                "rating":4.07,
                "owner":{
                    "id":45500,
                    "name":"Demo Owner"
                },
                "view":800000,
                "price":25.89,
                "type":"popular"
            }
        },
    )
    @validator('rating')
    def round_two_decimals(cls, v):
         return round(v, 2)
    @validator('price')
    def round_two_decimals(cls, v):
         return round(v, 2)

class UpdateOwner(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class UpdateCourseModel(BaseModel):
    name: Optional[str] = None
    rating: Optional[float] = None
    owner: Optional[UpdateOwner] = None
    view: Optional[int] = None
    price: Optional[float] = None
    type: Optional[Literal["recommended", "popular", "new", "nothing"]] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Demo Updated",
                "rating": 4.5,
                "owner": {
                    "id": 45500,
                    "name": "Updated Owner"
                },
                "view": 1000000,
                "price": 19.99,
                "type": "recommended"
            }
        },
    )

    @validator('rating')
    def round_rating(cls, v):
        return round(v, 2) if v is not None else v

    @validator('price')
    def round_price(cls, v):
        return round(v, 2) if v is not None else v