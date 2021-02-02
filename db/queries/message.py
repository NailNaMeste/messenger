from typing import List


from api.request import RequestPatchMsgDto
from api.request.create_message import RequestCreateMessageDto
from db.database import DBSession
from db.exceptions import DBEmployeeNotExistsException
from db.models.employee import DBMessage
from transport.sanic.exceptions import SanicMessageSelfSendingException


def create_message(session: DBSession, message: RequestCreateMessageDto, eid: int) -> DBMessage:
    new_message = DBMessage(
        user_message=message.user_message,
        recipient=message.recipient,
        recipient_id=session.get_recipient_id_by_login(message.recipient),
        sender_id=eid

    )

    if session.get_employee_by_login(new_message.recipient) is None:
        raise DBEmployeeNotExistsException

    session.add_model(new_message)

    return new_message


def get_message(session: DBSession, message_id: int) -> List['DBMessage']:
    db_message = session.get_message_by_id(message_id)

    return db_message


def patch_message(session: DBSession, message: RequestPatchMsgDto, message_id: int) -> DBMessage:
    db_message = session.get_message_by_id(message_id)
    for attr in message.fields:
        if hasattr(message, attr):
            value = getattr(message, attr)
            setattr(db_message, attr, value)

    return db_message


def delete_massage(session: DBSession, message_id: int) -> DBMessage:
    db_message = session.get_message_by_id(message_id)
    db_message.is_deleted = True
    return db_message


def get_messages_all(session: DBSession, eid: int) -> List['DBMessage']:

    list_db_message = session.get_all_messages_by_sender(eid)
    return list_db_message
