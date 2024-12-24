from fastapi import HTTPException,status


class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "server error"

    def __init__(self):
        
        super().__init__(status_code=self.STATUS_CODE,detail=self.DETAIL)

class CourseNotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Course is not found"


class CourseIsExists(DetailedHTTPException):
    STATUS_CODE=status.HTTP_400_BAD_REQUEST
    DETAIL = "Course is exists"

class CourseWithActiveRegistrationsException(DetailedHTTPException):
    STATUS_CODE = status.HTTP_406_NOT_ACCEPTABLE
    DETAIL = "It is not possible to delete because there is a student registered in this course."