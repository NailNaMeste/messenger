from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.create_message import RequestCreateMessageDto
from api.response import ResponseMessageDto
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicDBException, SanicMessageSelfSendingException
from db.queries import message as message_queries

from db.exceptions import DBDataException, DBIntegrityException


class CreateMessageEndpoint(BaseEndpoint):

    async def method_post(self, request: Request, body: dict, session, token: dict, *args, **kwargs) -> \
            BaseHTTPResponse:

        request_model = RequestCreateMessageDto(body)
        eid = token.get('eid')
        db_message = message_queries.create_message(session, request_model, eid)

        if db_message.sender_id == db_message.recipient_id:
            raise SanicMessageSelfSendingException("Cant send massage yourself")

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=201)

