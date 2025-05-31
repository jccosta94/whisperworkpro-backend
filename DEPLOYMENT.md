# 🚀 WhisperWorkPro Backend - Deployment Guide

## Quick Deployment to Render

### Step 1: Prepare Your Repository

1. **Initialize Git repository:**
```bash
cd /Users/joaocosta/Desktop/WhisperWorkPro-Backend
git init
git add .
git commit -m "Initial WhisperWorkPro backend setup"
```

2. **Create GitHub repository:**
   - Go to [GitHub](https://github.com) and create a new repository named `whisperworkpro-backend`
   - Don't initialize with README (we already have one)

3. **Push to GitHub:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/whisperworkpro-backend.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render

1. **Go to [Render.com](https://render.com)** and sign up/login

2. **Create New Web Service:**
   - Click "New" → "Web Service"
   - Connect your GitHub account
   - Select your `whisperworkpro-backend` repository

3. **Configure Service:**
   - **Name:** `whisperworkpro-api`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 10000`

4. **Set Environment Variables:**
   ```
   DATABASE_URL = postgresql://postgres:#Addidas123@db.lkxsnmolnhduuiuaaswb.supabase.co:5432/postgres
   ```

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment to complete (usually 2-3 minutes)

### Step 3: Test Your Deployment

Once deployed, your API will be available at: `https://YOUR_SERVICE_NAME.onrender.com`

Test endpoints:
- `GET https://YOUR_SERVICE_NAME.onrender.com/` - Health check
- `GET https://YOUR_SERVICE_NAME.onrender.com/docs` - API documentation

## Local Development Setup

### Prerequisites
- Python 3.11+
- pip

### Setup Instructions

1. **Clone or navigate to the project:**
```bash
cd /Users/joaocosta/Desktop/WhisperWorkPro-Backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set environment variable:**
```bash
export DATABASE_URL="postgresql://postgres:#Addidas123@db.lkxsnmolnhduuiuaaswb.supabase.co:5432/postgres"
```

5. **Run the application:**
```bash
uvicorn main:app --host 0.0.0.0 --port 10000 --reload
```

6. **Test the API:**
```bash
python test_api.py
```

## Using Docker (Alternative)

1. **Build the Docker image:**
```bash
docker build -t whisperworkpro-backend .
```

2. **Run the container:**
```bash
docker run -p 10000:10000 \
  -e DATABASE_URL="postgresql://postgres:#Addidas123@db.lkxsnmolnhduuiuaaswb.supabase.co:5432/postgres" \
  whisperworkpro-backend
```

## API Documentation

Once running, access the interactive API documentation at:
- Local: http://localhost:10000/docs
- Production: https://YOUR_SERVICE_NAME.onrender.com/docs

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `API_TITLE` | API title (optional) | No |
| `API_VERSION` | API version (optional) | No |

## Troubleshooting

### Common Issues

1. **Database connection error:**
   - Verify the DATABASE_URL is correct
   - Check if Supabase database is accessible

2. **Port issues:**
   - Render uses port 10000 by default
   - Ensure your start command matches

3. **Dependencies not installing:**
   - Check requirements.txt format
   - Ensure all dependencies are compatible

### Logs

On Render:
- Go to your service dashboard
- Click "Logs" to see real-time logs
- Check for any error messages

### Health Checks

Monitor your API health:
- `GET /health` - Returns server status
- `GET /` - Basic health check

## Next Steps

1. **Add Authentication:**
   - Implement JWT tokens
   - Add user management

2. **WhatsApp Integration:**
   - Connect WhatsApp Business API
   - Implement message sending

3. **Enhanced Features:**
   - File uploads
   - Email notifications
   - Reporting dashboard

## Support

- API Documentation: `/docs` endpoint
- GitHub Issues: Create issues in your repository
- Render Support: [Render Documentation](https://render.com/docs)

---

Your WhisperWorkPro backend is now ready for production! 🎉