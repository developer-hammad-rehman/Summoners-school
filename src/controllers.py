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