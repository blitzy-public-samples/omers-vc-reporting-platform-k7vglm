from sqlalchemy import Column, String, UUID, Enum, DECIMAL, Date, DateTime
from uuid import uuid4
from src.database.base import Base
from sqlalchemy.sql import func

# SQLAlchemy model version: ^1.4.0
# UUID version: ^3.9

class Company(Base):
    """
    SQLAlchemy model representing a company in the VC firm's portfolio
    
    Requirements addressed:
    - Company Data Model (2. SYSTEM ARCHITECTURE/2.2 Component Description/2.2.2 Data Layer)
    - Data Storage and Management (1. Introduction/1.2 Scope/Core Functionalities)
    """
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name = Column(String(255), nullable=False, index=True)
    reporting_status = Column(Enum("Active", "Inactive", "Pending", name="reporting_status"), nullable=False)
    reporting_currency = Column(String(3), nullable=False)
    fund = Column(String(100), nullable=False, index=True)
    location_country = Column(String(100), nullable=False)
    customer_type = Column(Enum("B2B", "B2C", "B2B2C", name="customer_type"), nullable=False)
    revenue_type = Column(Enum("Subscription", "Transactional", "Hybrid", name="revenue_type"), nullable=False)
    equity_raised = Column(DECIMAL(15, 2))
    post_money_valuation = Column(DECIMAL(15, 2))
    year_end_date = Column(Date, nullable=False)
    created_date = Column(DateTime, nullable=False, server_default=func.now())
    created_by = Column(String(100), nullable=False)
    last_update_date = Column(DateTime, onupdate=func.now())
    last_updated_by = Column(String(100))

    def __init__(self, **kwargs):
        """
        Initializes a new Company instance
        """
        super().__init__(**kwargs)

    def __repr__(self):
        """
        Returns a string representation of the Company instance
        """
        return f"<Company(id={self.id}, name='{self.name}', reporting_status='{self.reporting_status}')>"

    @classmethod
    def get_by_id(cls, session, company_id):
        """
        Retrieves a Company instance by its ID
        """
        return session.query(cls).filter(cls.id == company_id).first()

    @classmethod
    def get_by_name(cls, session, company_name):
        """
        Retrieves a Company instance by its name
        """
        return session.query(cls).filter(cls.name == company_name).first()

    def update(self, **kwargs):
        """
        Updates the Company instance with the provided keyword arguments
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self