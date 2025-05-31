from pydantic import BaseModel, validator, EmailStr
from typing import Optional, List
from datetime import datetime
import re

# Client schemas
class ClientBase(BaseModel):
    name: str
    phone_number: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    notes: Optional[str] = None

class ClientCreate(ClientBase):
    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip()
    
    @validator('phone_number')
    def validate_phone(cls, v):
        # Remove spaces and special characters, keep only digits and +
        phone = re.sub(r'[^\d+]', '', v)
        if not phone:
            raise ValueError('Phone number is required')
        if len(phone) < 10:
            raise ValueError('Phone number must be at least 10 digits')
        return phone

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    
    @validator('name')
    def validate_name(cls, v):
        if v is not None and len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip() if v else v
    
    @validator('phone_number')
    def validate_phone(cls, v):
        if v is not None:
            phone = re.sub(r'[^\d+]', '', v)
            if len(phone) < 10:
                raise ValueError('Phone number must be at least 10 digits')
            return phone
        return v

class ClientResponse(ClientBase):
    id: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Client Log schemas
class ClientLogBase(BaseModel):
    action: str
    details: Optional[str] = None
    performed_by: str

class ClientLogCreate(ClientLogBase):
    client_id: int

class ClientLogResponse(ClientLogBase):
    id: int
    client_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Merge clients schema
class MergeClientsRequest(BaseModel):
    primary_client_id: int
    secondary_client_id: int
    
    @validator('secondary_client_id')
    def validate_different_clients(cls, v, values):
        if 'primary_client_id' in values and v == values['primary_client_id']:
            raise ValueError('Primary and secondary client IDs must be different')
        return v

# Service schemas (for future use)
class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    base_price: Optional[str] = None

class ServiceCreate(ServiceBase):
    pass

class ServiceResponse(ServiceBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Job schemas (for future use)
class JobBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: Optional[str] = None
    scheduled_date: Optional[datetime] = None

class JobCreate(JobBase):
    client_id: int
    service_id: Optional[int] = None

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    price: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None

class JobResponse(JobBase):
    id: int
    client_id: int
    service_id: Optional[int] = None
    status: str
    completed_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Invoice schemas (for future use)
class InvoiceBase(BaseModel):
    amount: str
    due_date: Optional[datetime] = None

class InvoiceCreate(InvoiceBase):
    client_id: int
    job_id: Optional[int] = None
    invoice_number: str

class InvoiceUpdate(BaseModel):
    amount: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None
    paid_date: Optional[datetime] = None

class InvoiceResponse(InvoiceBase):
    id: int
    client_id: int
    job_id: Optional[int] = None
    invoice_number: str
    status: str
    sent_date: Optional[datetime] = None
    paid_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Response models for API operations
class MessageResponse(BaseModel):
    message: str

class MergeResponse(BaseModel):
    message: str
    primary_client: ClientResponse
    merged_data: List[str]