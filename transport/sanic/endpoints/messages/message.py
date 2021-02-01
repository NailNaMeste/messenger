from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestPatchMsgDto
from api.response import ResponseMessageDto
from db.database import DBSession
from db.exceptions import DBDataException, DBIntegrityException,\
     DBMessageNotExistException
from db.queries import message as message_queries
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicDBException, SanicMessageForbidden, SanicMessageReadNotAllowedException


class MessageEndpoint(BaseEndpoint):

    async def method_patch(
            self, request: Request, body: dict, session: DBSession, message_id: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:
        eid = token.get('eid')
        try:
            sender_id = session.get_message_by_id(message_id).sender_id
            if eid != sender_id:
                raise SanicMessageForbidden("Forbidden")
        except AttributeError:
            raise DBMessageNotExistException("Message not found")
        request_model = RequestPatchMsgDto(body)

        try:
            message = message_queries.patch_message(session, request_model, message_id)
        except AttributeError:
            raise DBMessageNotExistException('Message not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(message)

        return await self.make_response_json(status=200, body=response_model.dump())


    async def method_delete(
            self, request: Request, body: dict, session: DBSession, message_id: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:
        eid = token.get('eid')
        try:
            recipient_id = session.get_recipient_id_by_message(message_id)
            sender_id = session.get_message_by_id(message_id).sender_id
            if eid != sender_id and eid != recipient_id:
                raise SanicMessageForbidden("")
        except AttributeError:
            raise DBMessageNotExistException("Message not found")
        try:
            message = message_queries.delete_massage(session, message_id)
        except AttributeError:
            raise DBMessageNotExistException('message not found')

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        return await self.make_response_json(status=204)


    async def method_get(
            self, request: Request, body: dict, session: DBSession, message_id, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:
        eid = token.get('eid')

        try:
            recipient_id = session.get_recipient_id_by_message(message_id)
        except AttributeError:
            raise DBMessageNotExistException("Message not found")

        if eid != recipient_id:
            raise SanicMessageForbidden("Not allowed")
        try:
            db_message = message_queries.get_message(session, message_id)
        except SanicMessageReadNotAllowedException as e:
            raise e
        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump())
