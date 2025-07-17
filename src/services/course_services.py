from fastapi import HTTPException, Response ,status
from bson import ObjectId
from pymongo import ReturnDocument

from ..exceptions.base_exceptions import NotFoundException
from ..db.db_connector import db
from ..model.course_model import CourseModel, UpdateCourseModel



class CourseService:
    def __init__(self):
        self.course_collection  = db.get_collection("course")

    async def create_course(self,payload:CourseModel):
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
    
    async def get_course(self , course_id:str):
        course = await self.course_collection.find_one({"_id": ObjectId(course_id)})
        if not course:
            raise NotFoundException("Course Not Found")
        return course
    
    async def update_course(self , course_id:str , payload : UpdateCourseModel):
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
    
    async def delete_student(self,course_id: str):
        """
        Remove a single student record from the database.
        """
        delete_result = await self.course_collection.delete_one({"_id": ObjectId(course_id)})

        if delete_result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        raise NotFoundException(f"course {course_id} not found")
            