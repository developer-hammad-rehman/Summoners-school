from fastapi import APIRouter

from src.model.course_model import CourseModel
from ..controllers.course_controller import CourseController



course_router = APIRouter()

course_router.add_api_route('/create' , CourseController.create_course, methods=["POST"] , response_model=CourseModel)
course_router.add_api_route('/' , CourseController.get_courses , methods=["GET"] , response_model=list[CourseModel])
course_router.add_api_route("/search" , CourseController.get_course_by_name , methods=["GET"] , response_model=list[CourseModel])
course_router.add_api_route('/{course_id}' , CourseController.get_course , methods=["GET"] , response_model=CourseModel)
course_router.add_api_route('/update/{course_id}' , CourseController.update_course , methods=["PUT"] , response_model=CourseModel)
course_router.add_api_route('/delete/{course_id}' , CourseController.delete_course , methods=["DELETE"])
