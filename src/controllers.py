from src.model.course_model import CourseModel, UpdateCourseModel
from .exceptions.base_exceptions import BadRequest
from .utils.id_validator import isvalidate_id
from .model.guide_model import GuideModel, UpdateGuideModel
from .services import Service


class Controller:
    # --------------------- COURSE METHODS ---------------------

    @staticmethod
    async def create_course(course: CourseModel):
        return await Service().create_course(course)

    @staticmethod
    async def get_courses():
        return await Service().get_courses()

    @staticmethod
    async def get_course(course_id: str):
        isvalidate_id(course_id)
        return await Service().get_course(course_id)

    @staticmethod
    async def update_course(course_id: str, payload: UpdateCourseModel):
        isvalidate_id(course_id)
        return await Service().update_course(course_id, payload)

    @staticmethod
    async def delete_course(course_id: str):
        isvalidate_id(course_id)
        return await Service().delete_course(course_id)

    @staticmethod
    async def get_course_by_name(name: str):
        return await Service().search_course_by_name(name)

    # --------------------- GUIDE METHODS ---------------------

    @staticmethod
    async def create_guide(guide: GuideModel):
        return await Service().create_guide(guide)

    @staticmethod
    async def get_guides():
        return await Service().get_guides()

    @staticmethod
    async def get_guide(guide_id: str):
        isvalidate_id(guide_id)
        return await Service().get_guide(guide_id)

    @staticmethod
    async def update_guide(guide_id: str, payload: UpdateGuideModel):
        isvalidate_id(guide_id)
        return await Service().update_guide(guide_id, payload)

    @staticmethod
    async def delete_guide(guide_id: str):
        isvalidate_id(guide_id)
        return await Service().delete_guide(guide_id)

    @staticmethod
    async def get_guide_by_name(name: str):
        return await Service().search_guide_by_name(name)
