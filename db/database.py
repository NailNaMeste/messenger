from typing import List

from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import sessionmaker, Session, Query

from db.exceptions import DBIntegrityException, DBDataException
from db.models import BaseModel, DBEmployee, DBMessage


class DBSession:
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def query(self, *args, **kwargs) -> Query:
        return self._session.query(*args, **kwargs)

    def employees(self) -> Query:
        return self.query(DBEmployee).filter(DBEmployee.is_delete == 0)

    def messages(self) -> Query:
        return self.query(DBMessage)

    def close_session(self):
        self._session.close()

    def add_model(self, model: BaseModel):
        try:
            self._session.add(model)
        except IntegrityError as e:
            raise DBIntegrityException(e)
        except DataError as e:
            raise DBDataException(e)

    def get_employee_by_login(self, login: str) -> DBEmployee:
        return self.employees().filter(DBEmployee.login == login).first()

    def get_employee_by_id(self, eid: int) -> DBEmployee:
        return self.employees().filter(DBEmployee.id == eid).first()

    def get_recipient_id_by_login(self, recipient: str) -> DBMessage:
        return self.get_employee_by_login(recipient).id

    def get_message_by_sender(self, eid: int) -> DBMessage:
        return self.messages().filter(DBMessage.sender_id == eid)

    def get_all_messages_by_sender(self, eid: int) -> List[DBMessage]:
        return self.messages().filter(DBMessage.sender_id == eid).all()

    def get_message_by_recipient(self, message_id: int):
        return self.get_message_by_id(message_id).recipient_id

    def get_message_by_id(self, message_id: int) -> DBMessage:
        return self.messages().filter(DBMessage.id == message_id).first()

    def get_employee_all(self) -> List[DBEmployee]:
        qs = self.employees()
        return qs.all()

   # def get_msg(self, eid) -> List[DBMessage]:
      #  if self.get_sender_id(eid) == eid:


    def commit_session(self, need_close: bool = False):
        try:
            self._session.commit()
        except IntegrityError as e:
            raise DBIntegrityException(e)
        except DataError as e:
            raise DBDataException(e)

        if need_close:
            self.close_session()


class DataBase:
    connection: Engine
    session_factory: sessionmaker
    _test_query = 'SELECT 1'

    def __init__(self, connection: Engine):
        self.connection = connection
        self.session_factory = sessionmaker(bind=self.connection)

    def check_connection(self):
        self.connection.execute(self._test_query).fetchone()

    def make_session(self) -> DBSession:
        session = self.session_factory()
        return DBSession(session)
