from fastapi import HTTPException,status

class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "server error"

    def __init__(self):
        
        super().__init__(status_code=self.STATUS_CODE,detail=self.DETAIL)



class EndMarkNotFounded(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "End mark not founded"

class StudentNotRegisteredInCourse(DetailedHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "The student  has not registered for this course "


class AddedEndMark(DetailedHTTPException):
    STATUS_CODE = status.HTTP_405_METHOD_NOT_ALLOWED
    DETAIL = "End mark  has been entered for this student"