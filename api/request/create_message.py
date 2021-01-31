from marshmallow import Schema, fields

from api.base import RequestDto


class RequestCreateMessageDtoSchema(Schema):
    user_message = fields.Str(required=True, allow_none=False)
    recipient = fields.Str(required=True, allow_none=False)


class RequestCreateMessageDto(RequestDto, RequestCreateMessageDtoSchema):
    __schema__ = RequestCreateMessageDtoSchema
