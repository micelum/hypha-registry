from sqlalchemy import Column, String, Integer, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

class Model(base):
    __tablename__ = 'known_devices'

    id = Column(Integer, primary_key=True)
    machine_uuid = Column(String, nullable=False, unique=True)
    machine_mac = Column(String, nullable=False, unique=True)
    type = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
    is_active = Column(Boolean, default=True)
