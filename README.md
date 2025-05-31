# WhisperWorkPro Backend

FastAPI backend for WhisperWorkPro - A WhatsApp-native service CRM.

## Features

- ✅ Client management (CRUD operations)
- ✅ Client history tracking
- ✅ Merge duplicate clients
- ✅ Archive/restore clients
- ✅ Search functionality
- ✅ Resend invoices and job summaries
- ✅ RESTful API design
- ✅ Supabase PostgreSQL integration

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set environment variables:**
```bash
export DATABASE_URL="postgresql://postgres:#Addidas123@db.lkxsnmolnhduuiuaaswb.supabase.co:5432/postgres"
```

3. **Run the application:**
```bash
uvicorn main:app --host 0.0.0.0 --port 10000 --reload
```

4. **Test the API:**
```bash
python test_api.py
```

## API Endpoints

### Core Endpoints
- `GET /` - Health check
- `GET /health` - Detailed health status

### Client Management
- `POST /clients/` - Create new client
- `GET /clients/` - List all clients (with pagination)
- `GET /clients/{id}` - Get specific client
- `PUT /clients/{id}` - Update client
- `DELETE /clients/{id}` - Archive client (soft delete)
- `GET /clients/search/?q={query}` - Search clients

### Advanced Features
- `POST /clients/merge` - Merge two clients
- `GET /clients/{id}/history` - Get client activity history
- `POST /clients/{id}/resend-invoice` - Resend last invoice
- `POST /clients/{id}/resend-job-summary` - Resend job summary

## Database Schema

### Clients Table
- `id` - Primary key
- `name` - Client name (required)
- `phone_number` - Unique phone number (required)
- `email` - Email address (optional)
- `address` - Physical address (optional)
- `notes` - Additional notes (optional)
- `is_archived` - Soft delete flag
- `created_at` / `updated_at` - Timestamps

### Client Logs Table
- `id` - Primary key
- `client_id` - Foreign key to clients
- `action` - Action performed (created, updated, etc.)
- `details` - Action details
- `performed_by` - Who performed the action
- `created_at` - Timestamp

## Deployment on Render

1. **Push to GitHub:**
```bash
git init
git add .
git commit -m "Initial WhisperWorkPro backend"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

2. **Deploy on Render:**
   - Connect your GitHub repository
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 10000`
   - **Environment Variables:**
     ```
     DATABASE_URL = postgresql://postgres:#Addidas123@db.lkxsnmolnhduuiuaaswb.supabase.co:5432/postgres
     ```

## API Usage Examples

### Create a Client
```bash
curl -X POST "http://localhost:10000/clients/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "João Silva",
       "phone_number": "+351912345678",
       "email": "joao@example.com",
       "address": "Rua das Flores, 123, Porto"
     }'
```

### Search Clients
```bash
curl "http://localhost:10000/clients/search/?q=João"
```

### Get Client History
```bash
curl "http://localhost:10000/clients/1/history"
```

## Project Structure

```
WhisperWorkPro-Backend/
├── main.py              # FastAPI application
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic validation schemas
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── test_api.py         # API testing script
├── Dockerfile          # Docker configuration
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Features Ready for WhatsApp Integration

- Client phone number validation and normalization
- Resend invoice and job summary endpoints
- Complete audit trail for all client interactions
- Search functionality for quick client lookup
- Merge functionality for duplicate clients

## Development

### Running Tests
```bash
python test_api.py
```

### Using Docker
```bash
docker build -t whisperworkpro-backend .
docker run -p 10000:10000 -e DATABASE_URL="your_db_url" whisperworkpro-backend
```

## Next Steps

1. Deploy to Render using the instructions above
2. Integrate with WhatsApp Business API
3. Add authentication and user management
4. Implement invoice and job management endpoints
5. Add file upload capabilities for documents

## Support

For questions or support, check the API documentation at `http://localhost:10000/docs` when running locally.