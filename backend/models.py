from sqlalchemy import Column, Integer, String, Text

from database import Base


class ErrorEventModel(Base):
    __tablename__ = "error_events"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(String, nullable=False)
    app_name = Column(String, nullable=False)
    environment = Column(String, nullable=False)
    stack_trace = Column(Text, nullable=False)
    fingerprint = Column(String, nullable=False, index=True)
    occurrence_count = Column(Integer, nullable=False, default=1)