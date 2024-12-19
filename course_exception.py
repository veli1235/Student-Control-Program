from fastapi import HTTPException,status


class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "server error"

    def __init__(self):
        
        super().__init__(status_code=self.STATUS_CODE,detail=self.DETAIL)

class StudentNotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Student is not found"


class StudentIsExists(DetailedHTTPException):
    STATUS_CODE=status.HTTP_400_BAD_REQUEST
    DETAIL = "Student is exists"