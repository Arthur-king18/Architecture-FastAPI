from core.exceptions import CustomException


class PasswordDoesNotMatchException(CustomException):
    code = 401
    error_code = "USER__PASSWORD_DOES_NOT_MATCH"
    message = "password does not match"


class UserWrongPasswordException(CustomException):
    code = 401
    error_code = "USER__WRONG_PASSWORD"
    message = "wrong password"


class DuplicateEmailException(CustomException):
    code = 400
    error_code = "USER__DUPLICATE_EMAIL"
    message = "duplicate email"

class DuplicateUsernameException(CustomException):
    code = 400
    error_code = "USER__DUPLICATE_USERNAME"
    message = "duplicate username"

class UserNotValidEmail(CustomException):
    code = 400
    error_code = "USER__NOT_VALID_EMAIL"
    message = "user not valid email"

class UserNotFoundException(CustomException):
    code = 404
    error_code = "USER__NOT_FOUND"
    message = "user not found"

