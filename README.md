# ContentAI - LinkedIn Post Generator

## Environment Setup

1. Copy `.env.example` to `.env` in the backend directory:
```bash
cd ContentAI/backend
cp .env.example .env
```

2. Update the `.env` file with your credentials:
- MONGODB_URL: Your MongoDB connection URL
- MONGODB_NAME: Your database name
- OPENAI_API_KEY: Your OpenAI API key
- JWT_SECRET: A secure random string for JWT signing
- GOOGLE_CLIENT_ID: Your Google OAuth client ID

## Running the Application

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
