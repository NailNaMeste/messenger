from sanic.exceptions import SanicException


class DBIntegrityException(Exception):
    pass


class DBDataException(Exception):
    pass


class DBEmployeeExistsException(Exception):
    pass


class DBEmployeeNotExistsException(Exception):
    pass


class DBMessageSelfSendingException(Exception):
    pass


class DBMessageNotExistException(Exception):
    status_code = 404


class DBMessageReadNotAllowedException(SanicException):
    status_code = 400
