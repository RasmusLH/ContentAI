# ContentAI - LinkedIn Post Generator

An AI-powered tool that helps you create engaging LinkedIn posts using advanced AI technology.

## What it Does

- **Smart Post Generation**: Creates professional LinkedIn posts tailored to your needs
- **Multiple Templates**:
  - Tech Insights: Share technology trends and innovations
  - Startup Stories: Tell compelling startup journey narratives
  - Product Launches: Announce new products effectively 
  - Industry Updates: Share market trends and analysis

- **AI-Powered Features**:
  - Context-aware content generation
  - Professional tone adaptation
  - Automatic formatting for LinkedIn
  - Smart hashtag suggestions

- **User Features**:
  - Save and manage posts
  - Search through post history
  - Edit generated content
  - One-click copy to clipboard

- **Document Processing**:
  - Upload supporting documents
  - Extract relevant context
  - Support for TXT, DOC, DOCX files

## Security & Privacy

- Secure Google OAuth authentication
- Rate limiting to prevent abuse
- Data encryption in transit
- User data isolation

## Built With

- FastAPI & Python (Backend)
- React & TypeScript (Frontend)
- OpenAI GPT-4 API
- MongoDB Database

## Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ContentAI.git
cd ContentAI
```

2. Copy `.env.example` to `.env` in the backend directory:
```bash
cd backend
cp .env.example .env
```

3. Update the `.env` file with your credentials:
```
MONGODB_URL=mongodb://localhost:27017
MONGODB_NAME=contentai_db
OPENAI_API_KEY=your-openai-api-key
JWT_SECRET=your-jwt-secret-key
GOOGLE_CLIENT_ID=your-google-oauth-client-id
```

## Development Setup

### Backend

1. Create and activate virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
python main.py
```

The API will be available at http://localhost:8000

### Frontend

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Create `.env` file:
```
REACT_APP_GOOGLE_CLIENT_ID=your-google-oauth-client-id
```

3. Start development server:
```bash
npm start
```

The app will be available at http://localhost:3000

## Testing

### Backend Tests
```bash
cd backend
./run_tests.sh
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Project Structure

```
ContentAI/
├── backend/
│   ├── app/
│   │   ├── services/    # Business logic
│   │   ├── routes/      # API endpoints
│   │   └── utils/       # Helper functions
│   └── tests/           # Test suites
└── frontend/
    ├── src/
    │   ├── components/  # React components
    │   ├── contexts/    # React contexts
    │   ├── pages/       # Page components
    │   └── services/    # API integration
    └── public/          # Static assets
```

## License

This project is licensed under the MIT License.
