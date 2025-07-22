from fastapi import APIRouter

from src.model.course_model import CourseModel
from .controllers import Controller

router = APIRouter()

router.add_api_route(
    '/course/create',
    Controller.create_course,
    methods=["POST"],
    response_model=CourseModel,
    description="Create a new course by providing course data."
)

router.add_api_route(
    '/course/',
    Controller.get_courses,
    methods=["GET"],
    response_model=list[CourseModel],
    description="Retrieve a list of all courses."
)

router.add_api_route(
    '/course/search',
    Controller.get_course_by_name,
    methods=["GET"],
    response_model=list[CourseModel],
    description="Search for courses by name (case-insensitive). Use `?name=CourseName`."
)

router.add_api_route(
    '/course/{course_id}',
    Controller.get_course,
    methods=["GET"],
    response_model=CourseModel,
    description="Get a specific course by its unique ID."
)

router.add_api_route(
    '/course/update/{course_id}',
    Controller.update_course,
    methods=["PUT"],
    response_model=CourseModel,
    description="Update an existing course by its ID with the provided data."
)

router.add_api_route(
    '/course/delete/{course_id}',
    Controller.delete_course,
    methods=["DELETE"],
    description="Delete the course with the given ID."
)
