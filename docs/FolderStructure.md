---

# 📁 Project Folder Structure – Summoners School API

This FastAPI project is structured for scalability, clarity, and separation of concerns, following modern Python and backend development best practices.

---

## 🧾 Root Files

### `main.py` — Application Entry Point

Initializes the FastAPI application, registers exception handlers, and includes all route modules.

```python
from fastapi import FastAPI
from src.exceptions.handler import register_exception
from .routes import router

app = FastAPI(title="Summoners School")

register_exception(app)
app.include_router(router, prefix='/api')
```

---

## 🔁 `routes.py` — API Routes

Defines all the HTTP endpoints for interacting with the course resource.

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

## 🎮 `controllers.py` — Request Handlers

Controls how requests are handled and delegates logic to the service layer.

```python
from bson import ObjectId
from .exceptions.base_exceptions import BadRequest
from .utils.id_validator import isvalidate_id
from .model.course_model import CourseModel, UpdateCourseModel
from .services import CourseService

class CourseController:
    @staticmethod
    async def create_course(course: CourseModel):
        return await CourseService().create_course(course)

    @staticmethod
    async def get_courses():
        return await CourseService().get_courses()

    @staticmethod
    async def get_course(course_id: str):
        isvalidate_id(course_id)
        return await CourseService().get_course(course_id)

    @staticmethod
    async def update_course(course_id: str, payload: UpdateCourseModel):
        isvalidate_id(course_id)
        return await CourseService().update_course(course_id, payload)

    @staticmethod
    async def delete_course(course_id: str):
        isvalidate_id(course_id)
        return await CourseService().delete_course(course_id)

    @staticmethod 
    async def get_course_by_name(name: str):
        return await CourseService().search_by_name(name)
```

---

## 🧠 `services.py` — Business Logic Layer

Handles all application-specific logic and database interactions for courses.

```python
from fastapi import HTTPException, Response, status
from bson import ObjectId
from pymongo import ReturnDocument
from .exceptions.base_exceptions import NotFoundException
from .config.db_connector import db
from .model.course_model import CourseModel, UpdateCourseModel

class CourseService:
    def __init__(self):
        self.course_collection = db.get_collection("course")

    async def create_course(self, payload: CourseModel):
        new_course = await self.course_collection.insert_one(
            payload.model_dump(by_alias=True, exclude=["id"])
        )
        return await self.course_collection.find_one({"_id": new_course.inserted_id})

    async def get_courses(self):
        return await self.course_collection.find().to_list(length=None)

    async def get_course(self, course_id: str):
        course = await self.course_collection.find_one({"_id": ObjectId(course_id)})
        if not course:
            raise NotFoundException("Course Not Found")
        return course

    async def update_course(self, course_id: str, payload: UpdateCourseModel):
        update_fields = {k: v for k, v in payload.model_dump(by_alias=True).items() if v is not None}
        if update_fields:
            updated_course = await self.course_collection.find_one_and_update(
                {"_id": ObjectId(course_id)},
                {"$set": update_fields},
                return_document=ReturnDocument.AFTER,
            )
            if updated_course:
                return updated_course
            raise NotFoundException(f"Course {course_id} not found")
        
        existing_course = await self.course_collection.find_one({"_id": ObjectId(course_id)})
        if existing_course:
            return existing_course
        raise HTTPException(status_code=404, detail=f"Course {course_id} not found")

    async def delete_course(self, course_id: str):
        result = await self.course_collection.delete_one({"_id": ObjectId(course_id)})
        if result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        raise NotFoundException(f"Course {course_id} not found")

    async def search_by_name(self, name: str):
        cursor = self.course_collection.find({"name": name}).collation({"locale": "en", "strength": 2})
        return await cursor.to_list(length=None)
```

---

## 🧪 `utils/` — Helper Utilities

### `id_validator.py`

Validates if a given string is a valid MongoDB ObjectId.

```python
from bson import ObjectId
from ..exceptions.base_exceptions import BadRequest

def isvalidate_id(id: str):
    if not ObjectId.is_valid(id):
        print(id)
        raise BadRequest("Invalid ID Format")
```

---

## ⚙️ `config/` — Application Configuration

Handles MongoDB connection and environment loading.

### `db_connector.py`

```python
from motor.motor_asyncio import AsyncIOMotorClient
from .env_config import MONGODB_URI

client = AsyncIOMotorClient(MONGODB_URI)
db = client.get_database("summoners-school")
```

Automatically creates the database and collection when accessed.

### `env_config.py`

```python
from starlette.config import Config

try:
    config = Config('.env')
except FileNotFoundError:
    config = Config()

MONGODB_URI = config("MONGODB_URI", cast=str)
```

Loads environment variables from a `.env` file.

---

## ❗ `exceptions/` — Custom Exception Handling

### `base_exceptions.py`

```python
class NotFoundException(Exception):
    def __init__(self, detail: str, *args):
        super().__init__(*args)
        self.detail: str = detail

class BadRequest(Exception):
    def __init__(self, detail: str, *args):
        super().__init__(*args)
        self.detail: str = detail
```

### `handler.py`

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .base_exceptions import BadRequest, NotFoundException

def register_exception(app: FastAPI):
    @app.exception_handler(NotFoundException)
    async def not_found(request: Request, exc: NotFoundException):
        return JSONResponse(status_code=404, content={"detail": exc.detail})

    @app.exception_handler(BadRequest)
    async def bad_req_handler(req: Request, exc: BadRequest):
        return JSONResponse(status_code=400, content={"detail": exc.detail})
```

Registers custom exceptions with FastAPI for clean, consistent error responses.

---

## 🧩 `model/` — MongoDB Document Models

Defines the data schema used in MongoDB. Example model (not shown above) might look like:

```python
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class CourseModel(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    description: str
    price: float
    rating: float
    owner: dict
```

---

## ✅ Summary

| Folder/File      | Purpose                                                  |
| ---------------- | -------------------------------------------------------- |
| `main.py`        | FastAPI app initialization                               |
| `routes.py`      | API endpoints and routing                                |
| `controllers.py` | Controller methods for handling requests                 |
| `services.py`    | Business logic and MongoDB operations                    |
| `models/`        | MongoDB data models (schemas)                            |
| `config/`        | Environment and MongoDB configuration                    |
| `utils/`         | Reusable utility functions (e.g., ID validation)         |
| `exceptions/`    | Custom exceptions and FastAPI error handler registration |

---