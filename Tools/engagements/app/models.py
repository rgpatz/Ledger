from sqlalchemy import Column, Integer, String, DateTime, Date, Text, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class EngagementStatus(enum.Enum):
    PROPOSED = "Proposed"
    SCOPING = "Scoping"
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "In Progress"
    ON_HOLD = "On Hold"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False, unique=True)
    company = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    phone = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    contacts = relationship("ClientContact", back_populates="client", cascade="all, delete-orphan")
    engagements = relationship("Engagement", back_populates="client")

    def __repr__(self):
        return f"<Client(name='{self.name}', company='{self.company}')>"

class ClientContact(Base):
    __tablename__ = "client_contacts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    title = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    is_primary = Column(String, default="no", nullable=False)  # "yes" or "no" for compatibility
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    client = relationship("Client", back_populates="contacts")

    def __repr__(self):
        return f"<ClientContact(name='{self.name}', email='{self.email}')>"

class Engagement(Base):
    __tablename__ = "engagements"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    engagement_name = Column(String, index=True, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    client_name = Column(String, index=True, nullable=False)  # Keep for backward compatibility
    status = Column(SAEnum(EngagementStatus), default=EngagementStatus.PROPOSED, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    scope_summary = Column(Text, nullable=True)
    project_lead = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    client = relationship("Client", back_populates="engagements")

    def __repr__(self):
        return f"<Engagement(name='{self.engagement_name}', client='{self.client_name}')>" 