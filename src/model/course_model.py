from bson import ObjectId
from pydantic import BaseModel, Field , ConfigDict
from typing import Optional 
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class CourseModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    description: str 
    hours: int
    image_link: str = Field(..., alias="imageLink")
    short_video: str = Field(..., alias="shortVideo")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Demo",
                "description": "Demo",
                "hours": 10,
                "imageLink": "https://demo.example.com/images/demo.jpg",
                "shortVideo": "https://demo.example.com/videos/demo.mp4"
            }
        },
    )

class UpdateCourseModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None 
    hours: Optional[int] = None
    image_link: Optional[str] = None
    short_video : Optional[str] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Demo",
                "description": "Demo",
                "hours": 10,
                "imageLink": "https://demo.example.com/images/demo.jpg",
                "shortVideo": "https://demo.example.com/videos/demo.mp4"
            }
        },
    )
