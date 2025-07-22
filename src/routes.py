from fastapi import APIRouter
from src.model.course_model import CourseModel
from src.model.guide_model import GuideModel
from .controllers import Controller

router = APIRouter()

# ---------------------- COURSE ROUTES ----------------------

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

# ---------------------- GUIDE ROUTES ----------------------

router.add_api_route(
    '/guide/create',
    Controller.create_guide,
    methods=["POST"],
    response_model=GuideModel,
    description="Create a new guide by providing guide data."
)

router.add_api_route(
    '/guide/',
    Controller.get_guides,
    methods=["GET"],
    response_model=list[GuideModel],
    description="Retrieve a list of all guides."
)

router.add_api_route(
    '/guide/search',
    Controller.get_guide_by_name,
    methods=["GET"],
    response_model=list[GuideModel],
    description="Search for guides by name"
)

router.add_api_route(
    '/guide/{guide_id}',
    Controller.get_guide,
    methods=["GET"],
    response_model=GuideModel,
    description="Get a specific guide by its unique ID."
)

router.add_api_route(
    '/guide/update/{guide_id}',
    Controller.update_guide,
    methods=["PUT"],
    response_model=GuideModel,
    description="Update an existing guide by its ID with the provided data."
)

router.add_api_route(
    '/guide/delete/{guide_id}',
    Controller.delete_guide,
    methods=["DELETE"],
    description="Delete the guide with the given ID."
)
