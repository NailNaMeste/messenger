from sanic.exceptions import SanicException


class DBIntegrityException(Exception):
    pass


class DBDataException(Exception):
    pass


class DBEmployeeExistsException(Exception):
    pass


class DBEmployeeNotExistsException(Exception):
    pass


class DBMessageSelfSendingException(SanicException):
    pass


class DBMessageNotExistException(SanicException):
    status_code = 404



