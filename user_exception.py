from fastapi import HTTPException,status


class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "server error"

    def __init__(self):
        
        super().__init__(status_code=self.STATUS_CODE,detail=self.DETAIL)

class UserNotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "user is not found"


class UserIsExists(DetailedHTTPException):
    STATUS_CODE=status.HTTP_400_BAD_REQUEST
    DETAIL = "User is exists"


class WrongValue(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "enter the correct values" 


class WrongRole(DetailedHTTPException):
    STATUS_CODE = status.HTTP_405_METHOD_NOT_ALLOWED
    DETAIL = "This function is only for admins "

