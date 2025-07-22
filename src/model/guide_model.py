from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict, validator
from typing import Optional, Dict, Any
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]

class Owner(BaseModel):
    id: int
    name: str

class GuideModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    owner: Owner
    champion: str
    thumbnail: Optional[str] = None 
    playlist: Dict[str, Any] 
    description: Optional[str] = None
    content: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Top Lane Domination",
                "owner": {
                    "id": 1001,
                    "name": "CoachKing"
                },
                "champion": "Darius",
                "thumbnail": "https://example.com/thumbnail.png",
                "playlist": {
                    "intro": "https://example.com/intro.mp4",
                    "combos": "https://example.com/combos.mp4"
                },
                "description": "Learn to dominate top lane with Darius.",
                "content": "Detailed content here..."
            }
        }
    )

# Partial update model
class UpdateOwner(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class UpdateGuideModel(BaseModel):
    name: Optional[str] = None
    owner: Optional[UpdateOwner] = None
    champion: Optional[str] = None
    thumbnail: Optional[str] = None
    playlist: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    content: Optional[str] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Updated Top Lane Guide",
                "owner": {
                    "id": 1001,
                    "name": "CoachKingUpdated"
                },
                "champion": "Darius",
                "thumbnail": "https://example.com/new-thumb.png",
                "playlist": {
                    "intro": "https://example.com/updated-intro.mp4"
                },
                "description": "Updated Darius guide.",
                "content": "Updated content here..."
            }
        }
    )
