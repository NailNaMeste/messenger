from marshmallow import Schema, fields

from api.base import RequestDto


class RequestPatchMsgDtoSchema(Schema):
    user_message = fields.Str()


class RequestPatchMsgDto(RequestDto, RequestPatchMsgDtoSchema):
    fields: list
    __schema__ = RequestPatchMsgDtoSchema

    def __init__(self, *args, **kwargs):
        self.fields = []
        super(RequestPatchMsgDto, self).__init__(*args, **kwargs)

    def set(self, key, value):
        self.fields.append(key)
        super(RequestPatchMsgDto, self).set(key, value)
