from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, LargeBinary, Enum, Boolean
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from shared.core.enums import TaskStatus

Base = declarative_base()


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, ForeignKey("ocr_tasks.task_id"), nullable=False)
    image_bytes = Column(LargeBinary, nullable=False)
    text = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    ocr_task = relationship("OCRTask", back_populates="images")

class OCRTask(Base):
    __tablename__ = "ocr_tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, nullable=False, unique=True)
    status = Column(Enum(TaskStatus), nullable=False)
    batch = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    images = relationship("Image", back_populates="ocr_task", lazy="selectin")

