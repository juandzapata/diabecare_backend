from exceptions.custom_exception import CustomException


class NotCreatedException(CustomException):
    def __init__(self, message):
        super().__init__(message)
        