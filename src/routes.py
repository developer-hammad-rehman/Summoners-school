from fastapi import APIRouter

from src.model.course_model import CourseModel
from .controllers import CourseController



router = APIRouter()

router.add_api_route('/course/create' , CourseController.create_course, methods=["POST"] , response_model=CourseModel)
router.add_api_route('/course/' , CourseController.get_courses , methods=["GET"] , response_model=list[CourseModel])
router.add_api_route('/course/search' , CourseController.get_course_by_name , methods=["GET"] , response_model=list[CourseModel])
router.add_api_route('/course/{course_id}' , CourseController.get_course , methods=["GET"] , response_model=CourseModel)
router.add_api_route('/course/update/{course_id}' , CourseController.update_course , methods=["PUT"] , response_model=CourseModel)
router.add_api_route('/course/delete/{course_id}' , CourseController.delete_course , methods=["DELETE"])
