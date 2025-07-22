from fastapi import HTTPException, Response, status
from bson import ObjectId
from pymongo import ReturnDocument
from .exceptions.base_exceptions import NotFoundException
from .config.db_connector import db
from .model.course_model import CourseModel, UpdateCourseModel
from .model.guide_model import GuideModel, UpdateGuideModel  # Adjust path as needed


class Service:
    def __init__(self):
        """Initializes the Service with references to the course and guide MongoDB collections."""
        self.course_collection = db.get_collection("course")
        self.guide_collection = db.get_collection("guide")

    # ---------- COURSE OPERATIONS ----------

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
        update_data = {
            k: v for k, v in payload.model_dump(by_alias=True).items() if v is not None
        }
        if update_data:
            updated = await self.course_collection.find_one_and_update(
                {"_id": ObjectId(course_id)},
                {"$set": update_data},
                return_document=ReturnDocument.AFTER,
            )
            if updated:
                return updated
            raise NotFoundException(f"Course {course_id} not found")
        existing = await self.course_collection.find_one({"_id": ObjectId(course_id)})
        if existing:
            return existing
        raise HTTPException(status_code=404, detail=f"Course {course_id} not found")

    async def delete_course(self, course_id: str):
        result = await self.course_collection.delete_one({"_id": ObjectId(course_id)})
        if result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        raise NotFoundException(f"Course {course_id} not found")

    async def search_course_by_name(self, name: str):
        """
        Search courses by name using partial, case-insensitive matching.
        """
        cursor = self.course_collection.find(
            {"name": {"$regex": name, "$options": "i"}}
        )
        return await cursor.to_list(length=None)

    # ---------- GUIDE OPERATIONS ----------

    async def create_guide(self, payload: GuideModel):
        new_guide = await self.guide_collection.insert_one(
            payload.model_dump(by_alias=True, exclude=["id"])
        )
        return await self.guide_collection.find_one({"_id": new_guide.inserted_id})

    async def get_guides(self):
        return await self.guide_collection.find().to_list(length=None)

    async def get_guide(self, guide_id: str):
        guide = await self.guide_collection.find_one({"_id": ObjectId(guide_id)})
        if not guide:
            raise NotFoundException("Guide Not Found")
        return guide

    async def update_guide(self, guide_id: str, payload: UpdateGuideModel):
        update_data = {
            k: v for k, v in payload.model_dump(by_alias=True).items() if v is not None
        }
        if update_data:
            updated = await self.guide_collection.find_one_and_update(
                {"_id": ObjectId(guide_id)},
                {"$set": update_data},
                return_document=ReturnDocument.AFTER,
            )
            if updated:
                return updated
            raise NotFoundException(f"Guide {guide_id} not found")
        existing = await self.guide_collection.find_one({"_id": ObjectId(guide_id)})
        if existing:
            return existing
        raise HTTPException(status_code=404, detail=f"Guide {guide_id} not found")

    async def delete_guide(self, guide_id: str):
        result = await self.guide_collection.delete_one({"_id": ObjectId(guide_id)})
        if result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        raise NotFoundException(f"Guide {guide_id} not found")

    async def search_guide_by_name(self, name: str):
        """
        Search guides by name using partial, case-insensitive matching.
        """
        cursor = self.guide_collection.find(
            {"name": {"$regex": name, "$options": "i"}}
        )
        return await cursor.to_list(length=None)