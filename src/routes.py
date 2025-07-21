from fastapi import APIRouter

from src.model.course_model import CourseModel
from .controllers import Controller



router = APIRouter()

router.add_api_route('/course/create' , Controller.create_course, methods=["POST"] , response_model=CourseModel)
router.add_api_route('/course/' , Controller.get_courses , methods=["GET"] , response_model=list[CourseModel])
router.add_api_route('/course/search' , Controller.get_course_by_name , methods=["GET"] , response_model=list[CourseModel])
router.add_api_route('/course/{course_id}' , Controller.get_course , methods=["GET"] , response_model=CourseModel)
router.add_api_route('/course/update/{course_id}' , Controller.update_course , methods=["PUT"] , response_model=CourseModel)
router.add_api_route('/course/delete/{course_id}' , Controller.delete_course , methods=["DELETE"])
