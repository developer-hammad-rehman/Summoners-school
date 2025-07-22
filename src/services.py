from fastapi import HTTPException, Response, status
from bson import ObjectId
from pymongo import ReturnDocument
from .exceptions.base_exceptions import NotFoundException
from .config.db_connector import db
from .model.course_model import CourseModel, UpdateCourseModel


class Service:
    def __init__(self):
        """Initializes the Service with a reference to the course MongoDB collection."""
        self.course_collection = db.get_collection("course")

    async def create_course(self, payload: CourseModel):
        """
        Creates a new course document in the MongoDB collection.

        Args:
            payload (CourseModel): The course data to insert.

        Returns:
            dict: The created course document from the database.
        """
        new_course = await self.course_collection.insert_one(
            payload.model_dump(by_alias=True, exclude=["id"])
        )
        created_course = await self.course_collection.find_one(
            {"_id": new_course.inserted_id}
        )
        return created_course

    async def get_courses(self):
        """
        Retrieves all course documents from the collection.

        Returns:
            list: A list of all courses stored in the database.
        """
        courses = await self.course_collection.find().to_list(length=None)
        return courses

    async def get_course(self, course_id: str):
        """
        Retrieves a single course document by its ID.

        Args:
            course_id (str): The ObjectId of the course.

        Raises:
            NotFoundException: If the course is not found.

        Returns:
            dict: The course document from the database.
        """
        course = await self.course_collection.find_one({"_id": ObjectId(course_id)})
        if not course:
            raise NotFoundException("Course Not Found")
        return course

    async def update_course(self, course_id: str, payload: UpdateCourseModel):
        """
        Updates a course document with the provided fields.

        Args:
            course_id (str): The ObjectId of the course to update.
            payload (UpdateCourseModel): The fields to update.

        Raises:
            NotFoundException: If the course to update is not found.
            HTTPException: If course ID is invalid or update fails.

        Returns:
            dict: The updated course document.
        """
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
        raise HTTPException(status_code=404, detail=f"course {course_id} not found")

    async def delete_course(self, course_id: str):
        """
        Deletes a course document by its ID.

        Args:
            course_id (str): The ObjectId of the course to delete.

        Raises:
            NotFoundException: If no course is found to delete.

        Returns:
            Response: HTTP 204 No Content on success.
        """
        delete_result = await self.course_collection.delete_one(
            {"_id": ObjectId(course_id)}
        )

        if delete_result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        raise NotFoundException(f"course {course_id} not found")

    async def search_by_name(self, name: str):
        """
        Searches for courses by exact name match (case-insensitive).

        Args:
            name (str): The name of the course to search for.

        Returns:
            list: A list of matching course documents.
        """
        cursor = self.course_collection.find(
            {"name": name},
        ).collation({"locale": "en", "strength": 2})
        courses = await cursor.to_list(length=None)
        return courses
