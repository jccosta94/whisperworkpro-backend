from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    phone_number = Column(String(20), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=True, index=True)
    address = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    is_archived = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationship to logs
    logs = relationship("ClientLog", back_populates="client", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Client(id={self.id}, name='{self.name}', phone='{self.phone_number}')>"

class ClientLog(Base):
    __tablename__ = "client_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
    action = Column(String(50), nullable=False)  # created, updated, archived, merged, invoice_sent, etc.
    details = Column(Text, nullable=True)  # Additional details about the action
    performed_by = Column(String(255), nullable=False)  # Who performed the action
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationship to client
    client = relationship("Client", back_populates="logs")
    
    def __repr__(self):
        return f"<ClientLog(id={self.id}, client_id={self.client_id}, action='{self.action}')>"

# Additional models for future expansion
class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    base_price = Column(String(20), nullable=True)  # Store as string to handle currency formatting
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Service(id={self.id}, name='{self.name}')>"

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="pending", nullable=False)  # pending, in_progress, completed, cancelled
    price = Column(String(20), nullable=True)
    scheduled_date = Column(DateTime(timezone=True), nullable=True)
    completed_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    client = relationship("Client")
    service = relationship("Service")
    
    def __repr__(self):
        return f"<Job(id={self.id}, title='{self.title}', status='{self.status}')>"

class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True, index=True)
    invoice_number = Column(String(50), nullable=False, unique=True, index=True)
    amount = Column(String(20), nullable=False)
    status = Column(String(50), default="draft", nullable=False)  # draft, sent, paid, overdue, cancelled
    sent_date = Column(DateTime(timezone=True), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    paid_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    client = relationship("Client")
    job = relationship("Job")
    
    def __repr__(self):
        return f"<Invoice(id={self.id}, number='{self.invoice_number}', status='{self.status}')>"