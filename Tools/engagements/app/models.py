from sqlalchemy import Column, Integer, String, DateTime, Date, Text, Enum as SAEnum
from sqlalchemy.orm import declarative_base
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

class Engagement(Base):
    __tablename__ = "engagements"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    engagement_name = Column(String, index=True, nullable=False)
    client_name = Column(String, index=True, nullable=False)
    status = Column(SAEnum(EngagementStatus), default=EngagementStatus.PROPOSED, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    scope_summary = Column(Text, nullable=True)
    project_lead = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Engagement(name='{self.engagement_name}', client='{self.client_name}')>" 