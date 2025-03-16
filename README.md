# ContentAI - AI-Powered Content Generation Platform

A sophisticated content generation platform that leverages AI to create engaging social media posts, with a focus on professional content for platforms like LinkedIn. The application features a modern, responsive interface and robust backend architecture.

## 🚀 Key Features

- **AI-Powered Content Generation**
  - Text generation using advanced AI models
  - Image generation capabilities
  - Combined text and image post creation
  - Context-aware content adaptation

- **Multiple Content Types**
  - Professional social media posts
  - Technical insights and analysis
  - Product announcements
  - Industry updates
  - Custom templates for various content types

- **Advanced User Features**
  - Real-time content preview
  - Document upload and processing
  - Content history and management
  - Template-based generation
  - One-click content copying
  - Secure content saving

- **Professional Integration**
  - Google OAuth authentication
  - Secure API endpoints
  - Rate limiting and abuse prevention
  - Data encryption and security

## 🛠️ Technical Stack

### Frontend Technologies
- **Core Framework**
  - React 18 with TypeScript
  - Modern React Hooks and Context API
  - Type-safe development with TypeScript

- **Styling & UI**
  - Custom CSS with modern flexbox/grid layouts
  - Responsive design principles
  - Component-based architecture

- **State Management & API Integration**
  - Custom React Context for state management
  - Axios for API communication
  - Type-safe API integration

### Backend Technologies
- **Core Framework**
  - FastAPI (Python)
  - RESTful API architecture
  - Async/await pattern support

- **Database & Storage**
  - MongoDB for data persistence
  - File storage system for documents

- **AI Integration**
  - OpenAI API integration
  - Custom AI processing pipeline
  - Intelligent content generation algorithms

### DevOps & Infrastructure
- **Containerization**
  - Docker with multi-stage builds
  - Docker Compose for development and production
  - Nginx reverse proxy configuration

- **CI/CD**
  - GitHub Actions workflows
  - Automated testing and deployment
  - Environment-specific configurations

- **Security**
  - JWT authentication
  - OAuth 2.0 integration
  - Environment-based secrets management

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 16+ and npm
- Python 3.8+
- MongoDB instance

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ContentAI.git
cd ContentAI
```

2. Set up environment variables:
```bash
# Backend
cp backend/.env.example backend/.env
# Update the .env file with your credentials

# Frontend
cp frontend/.env.example frontend/.env
```

3. Start the development environment:
```bash
docker-compose up
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Production Deployment

For production deployment:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 📚 Project Structure

```
ContentAI/
├── frontend/                # React TypeScript frontend
│   ├── src/
│   │   ├── components/     # Reusable React components
│   │   ├── contexts/       # React Context providers
│   │   ├── services/       # API integration services
│   │   ├── types/         # TypeScript type definitions
│   │   └── utils/         # Utility functions
│   └── public/            # Static assets
├── backend/               # FastAPI Python backend
│   ├── app/
│   │   ├── routes/       # API endpoints
│   │   ├── services/     # Business logic
│   │   └── utils/        # Helper functions
│   └── tests/            # Test suites
├── nginx/                # Nginx configuration
└── .github/workflows/    # CI/CD pipelines
```

## 🧪 Testing

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. 