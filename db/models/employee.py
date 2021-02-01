from sqlalchemy import Column, VARCHAR, BOOLEAN, INT, LargeBinary

from db.models import BaseModel


class DBEmployee(BaseModel):

    __tablename__ = 'employees'

    login = Column(VARCHAR(20), unique=True, nullable=False)
    password = Column(LargeBinary(), nullable=False)
    first_name = Column(VARCHAR(50))
    last_name = Column(VARCHAR(50))
    is_delete = Column(BOOLEAN(), nullable=False, default=False)


class DBMessage(BaseModel):
    __tablename__ = 'message'

    user_message = Column(VARCHAR(200), nullable=False)
    recipient = Column(VARCHAR(50), nullable=False)
    sender_id = Column(INT, nullable=False)
    recipient_id = Column(INT, nullable=False)
    is_deleted = Column(BOOLEAN(), nullable=False, default=False)
