from bson import ObjectId
from .exceptions.base_exceptions import BadRequest
from .utils.id_validator import isvalidate_id
from .model.course_model import CourseModel, UpdateCourseModel
from .services import Service


class Controller:
    @staticmethod
    async def create_course(course: CourseModel):
        """
        Create a new course in the database.

        Args:
            course (CourseModel): The course data to be inserted.

        Returns:
            dict: The created course document.
        """
        result = await Service().create_course(course)
        return result

    @staticmethod
    async def get_courses():
        """
        Retrieve all courses from the database.

        Returns:
            list: A list of all course documents.
        """
        result = await Service().get_courses()
        return result

    @staticmethod
    async def get_course(course_id: str):
        """
        Retrieve a specific course by its ID.

        Args:
            course_id (str): The unique ID of the course.

        Raises:
            BadRequest: If the course ID is invalid.

        Returns:
            dict: The course document if found.
        """
        isvalidate_id(course_id)
        result = await Service().get_course(course_id)
        return result

    @staticmethod
    async def update_course(course_id: str, payload: UpdateCourseModel):
        """
        Update a course's details based on the given payload.

        Args:
            course_id (str): The ID of the course to update.
            payload (UpdateCourseModel): Fields to update.

        Raises:
            BadRequest: If the course ID is invalid.

        Returns:
            dict: The updated course document.
        """
        isvalidate_id(course_id)
        result = await Service().update_course(course_id, payload)
        return result

    @staticmethod
    async def delete_course(course_id: str):
        """
        Delete a course from the database using its ID.

        Args:
            course_id (str): The ID of the course to delete.

        Raises:
            BadRequest: If the course ID is invalid.

        Returns:
            Response: HTTP 204 No Content on successful deletion.
        """
        isvalidate_id(course_id)
        return await Service().delete_course(course_id)

    @staticmethod
    async def get_course_by_name(name: str):
        """
        Search for courses that match the given name (case-insensitive).

        Args:
            name (str): Name of the course to search.

        Returns:
            list: List of matched course documents.
        """
        return await Service().search_by_name(name)
