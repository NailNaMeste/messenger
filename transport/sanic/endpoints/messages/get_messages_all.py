from sanic.request import Request
from sanic.response import BaseHTTPResponse
from sanic.exceptions import SanicException
from api.response import  ResponseMessageDto
from db.database import DBSession
from db.queries import message as message_queries

from transport.sanic.endpoints import BaseEndpoint


class AllMsgEndpoint(BaseEndpoint):

    async def method_get(
            self, request: Request, body: dict, session: DBSession, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:
        eid = token.get('eid')

        db_message = message_queries.get_messages_all(session, eid)

        response_model = ResponseMessageDto(db_message, many=True)

        return await self.make_response_json(status=200, body=response_model.dump())
