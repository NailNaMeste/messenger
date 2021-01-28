from marshmallow import Schema, fields

from api.base import RequestDto


class RequestGetEmployeeDtoSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()
    login = fields.Str()
    created_at = fields.Str()
    updated_at = fields.Str()


class RequestGetEmployeeDto(RequestDto, RequestGetEmployeeDtoSchema):
    __schema__ = RequestGetEmployeeDtoSchema
