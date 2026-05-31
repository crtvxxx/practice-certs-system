import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class UserRole(str, enum.Enum):
    STUDENT = "student"
    STAFF = "staff"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
    orders = relationship("Order", back_populates="user")

class CertificateType(str, enum.Enum):
    STUDY = "справка об обучении"
    MILITARY = "справка для военкомата"
    SOCIAL = "справка для соцзащиты"

class OrderStatus(str, enum.Enum):
    NEW = "принято"
    PROCESSING = "выполняется"
    READY = "готово"

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    certificate_type = Column(Enum(CertificateType), nullable=False)
    reason = Column(String, default="")
    status = Column(Enum(OrderStatus), default=OrderStatus.NEW)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="orders")