from sqlalchemy import Integer, Column, DateTime, String, ForeignKey

from makers.apps.db.abstract import IDBase


class TokenBlocklist(IDBase):
    jti = Column(String(256), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
