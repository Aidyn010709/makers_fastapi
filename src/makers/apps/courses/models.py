from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, String, DateTime, 
    Enum, Integer, ForeignKey, 
    SMALLINT, BOOLEAN, Text, BigInteger,
    Time
)
from makers.apps.db.abstract import IDBase, TimestampBase

    
class Course(IDBase, TimestampBase):
    __tablename__ = "courses"
    
    user_id = Column(BigInteger,
                     ForeignKey("mentors.id", ondelete="SET NULL"),
                     info={"verbose_name": "ID владельца курса"})
    title = Column(String(128),
                          info={"verbose_name": "Название курса"})
    description = Column(Text,
                         info={"verbose_name": "Описание"})
    duration = Column(SMALLINT,
                      info={"verbose_name": "Длительность курса"})
    start_date = Column(DateTime,
                        info={"verbose_name": "Дата начала курса"})
    price = Column(SMALLINT,
                   info={"verbose_name": "Цена с одного человека"})

    is_active = Column(BOOLEAN, default=False)
    is_deactivated = Column(BOOLEAN, default=True)

    # relationships
    user = relationship("Mentor")
