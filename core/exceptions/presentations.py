from core.exceptions import CustomException


class PresentationNotGenerateException(CustomException):
    code = 404
    error_code = "PRESENTATIONS__NOT_GENERATE"
    message = "presentations not generate"

class TextNotGenerateException(CustomException):
    code = 404
    error_code = "TEXT__NOT_GENERATE"
    message = "text not generate"


