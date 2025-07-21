---

# 📁 Project Structure: Summoners School API

This FastAPI project follows a clean, modular architecture designed for scalability, maintainability, and developer productivity.

---

## 🧾 Root Structure Overview

```
summoners-school/
│
├── main.py
├── routes.py
├── controllers.py
├── services.py
│
├── config/
│   ├── db_connector.py
│   └── env_config.py
│
├── exceptions/
│   ├── base_exceptions.py
│   └── handler.py
│
├── model/
│   └── course_model.py
│
├── utils/
│   └── id_validator.py
│
├── .env
└── requirements.txt
```

---

## 📌 File/Folder Descriptions

### 🔹 `main.py` – App Entry Point

Initializes the FastAPI app, registers exception handlers, and includes all route modules.

```python
from fastapi import FastAPI
from src.exceptions.handler import register_exception
from .routes import router

app = FastAPI(title="Summoners School")

register_exception(app)
app.include_router(router, prefix='/api')
```

---

### 🔹 `routes.py` – API Route Definitions

All HTTP endpoints related to course management.

```python
from fastapi import APIRouter
from src.model.course_model import CourseModel
from .controllers import CourseController

router = APIRouter()

router.add_api_route('/course/create', CourseController.create_course, methods=["POST"], response_model=CourseModel)
router.add_api_route('/course/', CourseController.get_courses, methods=["GET"], response_model=list[CourseModel])
router.add_api_route('/course/search', CourseController.get_course_by_name, methods=["GET"], response_model=list[CourseModel])
router.add_api_route('/course/{course_id}', CourseController.get_course, methods=["GET"], response_model=CourseModel)
router.add_api_route('/course/update/{course_id}', CourseController.update_course, methods=["PUT"], response_model=CourseModel)
router.add_api_route('/course/delete/{course_id}', CourseController.delete_course, methods=["DELETE"])
```

---

### 🔹 `controllers.py` – Controller Layer

Handles incoming requests, performs input validation, and delegates logic to the service layer.

```python
from bson import ObjectId
from .exceptions.base_exceptions import BadRequest
from .utils.id_validator import isvalidate_id
from .model.course_model import CourseModel, UpdateCourseModel
from .services import Service


class Controller:
    @staticmethod
    async def create_course(course: CourseModel):
        result = await Service().create_course(course)
        return result

    @staticmethod
    async def get_courses():
        result = await Service().get_courses()
        return result

    @staticmethod
    async def get_course(course_id: str):
        isvalidate_id(course_id)
        result = await Service().get_course(course_id)
        return result

    @staticmethod
    async def update_course(course_id: str, payload: UpdateCourseModel):
        isvalidate_id(course_id)
        result = await Service().update_course(course_id, payload)
        return result

    @staticmethod
    async def delete_course(course_id: str):
        isvalidate_id(course_id)
        return await Service().delete_course(course_id)
    @staticmethod
    async def get_course_by_name(name: str):
        return await Service().search_by_name(name)
```

---

### 🔹 `services.py` – Business Logic Layer

Interacts with the MongoDB collection and implements core business operations.

```python
from fastapi import HTTPException, Response, status
from bson import ObjectId
from pymongo import ReturnDocument
from .exceptions.base_exceptions import NotFoundException
from .config.db_connector import db
from .model.course_model import CourseModel, UpdateCourseModel


class Service:
    def __init__(self):
        self.course_collection = db.get_collection("course")

    async def create_course(self, payload: CourseModel):
        new_course = await self.course_collection.insert_one(
            payload.model_dump(by_alias=True, exclude=["id"])
        )
        created_course = await self.course_collection.find_one(
            {"_id": new_course.inserted_id}
        )
        return created_course

    async def get_courses(self):
        courses = await self.course_collection.find().to_list(length=None)
        return courses

    async def get_course(self, course_id: str):
        course = await self.course_collection.find_one({"_id": ObjectId(course_id)})
        if not course:
            raise NotFoundException("Course Not Found")
        return course

    async def update_course(self, course_id: str, payload: UpdateCourseModel):
        course = {
            k: v for k, v in payload.model_dump(by_alias=True).items() if v is not None
        }
        if len(course) >= 1:
            update_result = await self.course_collection.find_one_and_update(
                {"_id": ObjectId(course_id)},
                {"$set": course},
                return_document=ReturnDocument.AFTER,
            )
            if update_result is not None:
                return update_result
            else:
                raise NotFoundException(f"course {course_id} not found")
        existing_course = await self.course_collection.find_one({"_id": course_id})
        if existing_course is not None:
            return existing_course
        raise HTTPException(status_code=404, detail=f"course {id} not found")

    async def delete_course(self, course_id: str):
        delete_result = await self.course_collection.delete_one(
            {"_id": ObjectId(course_id)}
        )

        if delete_result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        raise NotFoundException(f"course {course_id} not found")

    async def search_by_name(self, name: str):
        cursor = self.course_collection.find(
            {"name": name},
        ).collation({"locale": "en", "strength": 2})
        courses = await cursor.to_list(length=None)
        return courses
```

---

### 🔹 `model/course_model.py` – MongoDB Course Schema

Defines both full and partial schemas for the course collection.

```python
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict, validator
from typing import Literal, Optional
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class Owner(BaseModel):
    id: int
    name: str

class CourseModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    rating: float
    owner: Owner
    view: int
    price: float
    type: Literal["recommended", "popular", "new", "nothing"]

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Demo",
                "rating": 4.07,
                "owner": {"id": 45500, "name": "Demo Owner"},
                "view": 800000,
                "price": 25.89,
                "type": "popular"
            }
        }
    )

    @validator('rating')
    def round_rating(cls, v): return round(v, 2)

    @validator('price')
    def round_price(cls, v): return round(v, 2)

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
                "owner": {"id": 45500, "name": "Updated Owner"},
                "view": 1000000,
                "price": 19.99,
                "type": "recommended"
            }
        }
    )

    @validator('rating')
    def round_rating(cls, v): return round(v, 2) if v is not None else v

    @validator('price')
    def round_price(cls, v): return round(v, 2) if v is not None else v
```

---

### 🔹 `utils/id_validator.py` – ObjectId Validation

```python
from bson import ObjectId
from ..exceptions.base_exceptions import BadRequest

def isvalidate_id(id: str):
    if not ObjectId.is_valid(id):
        print(id)
        raise BadRequest("Invalid ID Format")
```

---

### 🔹 `config/db_connector.py` – MongoDB Connection

```python
from motor.motor_asyncio import AsyncIOMotorClient
from .env_config import MONGODB_URI

client = AsyncIOMotorClient(MONGODB_URI)
db = client.get_database("summoners-school")
```

### 🔹 `config/env_config.py` – Load Environment Variables

```python
from starlette.config import Config

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

MONGODB_URI = config("MONGODB_URI", cast=str)
```

---

### 🔹 `exceptions/base_exceptions.py` – Custom Exceptions

```python
class NotFoundException(Exception):
    def __init__(self, detail: str, *args):
        super().__init__(*args)
        self.detail = detail

class BadRequest(Exception):
    def __init__(self, detail: str, *args):
        super().__init__(*args)
        self.detail = detail
```

---

### 🔹 `exceptions/handler.py` – Exception Handlers

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .base_exceptions import BadRequest, NotFoundException

def register_exception(app: FastAPI):
    @app.exception_handler(NotFoundException)
    async def not_found(request: Request, exc: NotFoundException):
        return JSONResponse(status_code=404, content={"detail": exc.detail})

    @app.exception_handler(BadRequest)
    async def bad_request(request: Request, exc: BadRequest):
        return JSONResponse(status_code=400, content={"detail": exc.detail})
```

---