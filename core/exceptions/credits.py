from core.exceptions import CustomException

class CreditsNotEnoughException(CustomException):
    code = 402
    error_code = "CREDITS__ARE_NOT_ENOUGH"
    message = "credits are not enough"