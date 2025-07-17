from bson import ObjectId
from ..exceptions.base_exceptions import BadRequest
from ..utils.id_validator import isvalidate_id
from ..model.course_model import CourseModel, UpdateCourseModel
from ..services.course_services import CourseService


class CourseController:
    @staticmethod
    async def create_course(course: CourseModel):
        result = await CourseService().create_course(course)
        return result

    @staticmethod
    async def get_courses():
        result = await CourseService().get_courses()
        return result

    @staticmethod
    async def get_course(course_id: str):
        isvalidate_id(course_id)
        result = await CourseService().get_course(course_id)
        return result

    @staticmethod
    async def update_course(course_id: str, payload: UpdateCourseModel):
        isvalidate_id(course_id)
        result = await CourseService().update_course(course_id, payload)
        return result

    @staticmethod
    async def delete_course(course_id: str):
        isvalidate_id(course_id)
        return await CourseService().delete_student(course_id)
