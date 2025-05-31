from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, Optional
import os
from models import Client, ClientLog, Base
from schemas import ClientCreate, ClientUpdate, ClientResponse, ClientLogResponse, MergeClientsRequest
import uvicorn

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:#Addidas123@db.lkxsnmolnhduuiuaaswb.supabase.co:5432/postgres")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title="WhisperWorkPro API",
    description="WhatsApp-native service CRM backend",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "WhisperWorkPro API is running!", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Client endpoints
@app.post("/clients/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    """Create a new client"""
    try:
        # Check if client with phone already exists
        existing_client = db.query(Client).filter(Client.phone_number == client.phone_number).first()
        if existing_client and not existing_client.is_archived:
            raise HTTPException(
                status_code=400, 
                detail="Active client with this phone number already exists"
            )
        
        db_client = Client(**client.dict())
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        
        # Log the creation
        log_entry = ClientLog(
            client_id=db_client.id,
            action="created",
            details=f"Client {db_client.name} created",
            performed_by="system"
        )
        db.add(log_entry)
        db.commit()
        
        return db_client
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/clients/", response_model=List[ClientResponse])
async def get_clients(
    skip: int = 0, 
    limit: int = 100, 
    include_archived: bool = False,
    db: Session = Depends(get_db)
):
    """Get all clients with pagination"""
    query = db.query(Client)
    if not include_archived:
        query = query.filter(Client.is_archived == False)
    
    clients = query.offset(skip).limit(limit).all()
    return clients

@app.get("/clients/{client_id}", response_model=ClientResponse)
async def get_client(client_id: int, db: Session = Depends(get_db)):
    """Get a specific client by ID"""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@app.put("/clients/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int, 
    client_update: ClientUpdate, 
    db: Session = Depends(get_db)
):
    """Update a client"""
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        # Store original values for logging
        original_values = {
            "name": client.name,
            "phone_number": client.phone_number,
            "email": client.email,
            "address": client.address
        }
        
        # Update fields
        update_data = client_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(client, field, value)
        
        client.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(client)
        
        # Log the update
        changes = []
        for field, new_value in update_data.items():
            if field in original_values and original_values[field] != new_value:
                changes.append(f"{field}: '{original_values[field]}' → '{new_value}'")
        
        if changes:
            log_entry = ClientLog(
                client_id=client.id,
                action="updated",
                details=f"Client updated: {', '.join(changes)}",
                performed_by="system"
            )
            db.add(log_entry)
            db.commit()
        
        return client
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/clients/{client_id}")
async def archive_client(client_id: int, db: Session = Depends(get_db)):
    """Archive a client (soft delete)"""
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        client.is_archived = True
        client.updated_at = datetime.utcnow()
        db.commit()
        
        # Log the archival
        log_entry = ClientLog(
            client_id=client.id,
            action="archived",
            details=f"Client {client.name} archived",
            performed_by="system"
        )
        db.add(log_entry)
        db.commit()
        
        return {"message": "Client archived successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clients/merge")
async def merge_clients(merge_request: MergeClientsRequest, db: Session = Depends(get_db)):
    """Merge two clients"""
    try:
        primary_client = db.query(Client).filter(Client.id == merge_request.primary_client_id).first()
        secondary_client = db.query(Client).filter(Client.id == merge_request.secondary_client_id).first()
        
        if not primary_client or not secondary_client:
            raise HTTPException(status_code=404, detail="One or both clients not found")
        
        if primary_client.id == secondary_client.id:
            raise HTTPException(status_code=400, detail="Cannot merge a client with itself")
        
        # Merge logic - update primary client with secondary client's data if fields are empty
        merge_fields = ["email", "address", "notes"]
        merged_data = []
        
        for field in merge_fields:
            primary_value = getattr(primary_client, field)
            secondary_value = getattr(secondary_client, field)
            
            if not primary_value and secondary_value:
                setattr(primary_client, field, secondary_value)
                merged_data.append(f"{field}: '{secondary_value}'")
        
        # Archive the secondary client
        secondary_client.is_archived = True
        secondary_client.updated_at = datetime.utcnow()
        primary_client.updated_at = datetime.utcnow()
        
        db.commit()
        
        # Log the merge
        log_entry = ClientLog(
            client_id=primary_client.id,
            action="merged",
            details=f"Merged with client {secondary_client.name} (ID: {secondary_client.id}). " + 
                   f"Inherited: {', '.join(merged_data) if merged_data else 'no new data'}",
            performed_by="system"
        )
        db.add(log_entry)
        
        secondary_log_entry = ClientLog(
            client_id=secondary_client.id,
            action="merged_into",
            details=f"Merged into client {primary_client.name} (ID: {primary_client.id})",
            performed_by="system"
        )
        db.add(secondary_log_entry)
        db.commit()
        
        return {
            "message": "Clients merged successfully",
            "primary_client": primary_client,
            "merged_data": merged_data
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/clients/{client_id}/history", response_model=List[ClientLogResponse])
async def get_client_history(client_id: int, db: Session = Depends(get_db)):
    """Get client history/logs"""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    logs = db.query(ClientLog).filter(ClientLog.client_id == client_id).order_by(ClientLog.created_at.desc()).all()
    return logs

@app.post("/clients/{client_id}/resend-invoice")
async def resend_last_invoice(client_id: int, db: Session = Depends(get_db)):
    """Resend last invoice to client"""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # In a real implementation, you would:
    # 1. Query the last invoice for this client
    # 2. Send it via WhatsApp API
    # 3. Log the action
    
    # For now, we'll just log the action
    log_entry = ClientLog(
        client_id=client_id,
        action="invoice_resent",
        details=f"Last invoice resent to {client.name}",
        performed_by="system"
    )
    db.add(log_entry)
    db.commit()
    
    return {"message": f"Invoice resent to {client.name} at {client.phone_number}"}

@app.post("/clients/{client_id}/resend-job-summary")
async def resend_job_summary(client_id: int, db: Session = Depends(get_db)):
    """Resend last job summary to client"""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # In a real implementation, you would:
    # 1. Query the last job/service for this client
    # 2. Generate summary
    # 3. Send it via WhatsApp API
    # 4. Log the action
    
    # For now, we'll just log the action
    log_entry = ClientLog(
        client_id=client_id,
        action="job_summary_resent",
        details=f"Last job summary resent to {client.name}",
        performed_by="system"
    )
    db.add(log_entry)
    db.commit()
    
    return {"message": f"Job summary resent to {client.name} at {client.phone_number}"}

# Search endpoint
@app.get("/clients/search/", response_model=List[ClientResponse])
async def search_clients(
    q: str,
    include_archived: bool = False,
    db: Session = Depends(get_db)
):
    """Search clients by name, phone, or email"""
    query = db.query(Client)
    if not include_archived:
        query = query.filter(Client.is_archived == False)
    
    # Search in name, phone_number, and email
    search_filter = (
        Client.name.ilike(f"%{q}%") |
        Client.phone_number.ilike(f"%{q}%") |
        Client.email.ilike(f"%{q}%")
    )
    
    clients = query.filter(search_filter).limit(50).all()
    return clients

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)