# Database Models
from sqlalchemy import Column, String, Text
import uuid
from database import Base


class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    query = Column(Text, nullable=False)
    result = Column(Text, nullable=False)
    file_name = Column(String, nullable=True)