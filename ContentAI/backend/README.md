# ContentAI Backend

The backend service powering the LinkedIn Post Generator application.

## Features

### Content Generation
- Advanced text generation using OpenAI GPT-4
- Smart template system for different post types
- Context-aware content adaptation
- Document processing and text extraction

### API Endpoints
- Post generation with file upload support
- User authentication and session management
- Post history with search capability
- Save/delete functionality for posts

### Security
- Rate limiting protection
- File validation and sanitization
- Secure authentication flow
- MongoDB data persistence

### Performance
- Async/await architecture
- Efficient database queries
- Request caching
- Optimized file processing

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ContentAI.git
cd ContentAI/backend
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the `backend` directory and add the necessary environment variables:
```
MONGO_URI=<your_mongo_uri>
OPENAI_API_KEY=<your_openai_api_key>
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

### Windows-Specific Setup

If you're running on Windows, you'll need additional steps for file validation:

1. Install the Windows requirements:
```bash
pip install python-magic-bin
```

2. If you encounter any issues, you can alternatively:
   - Download the DLL files from [here](https://github.com/julian-r/python-magic/files/9040285/magic.zip)
   - Extract the DLL files to `C:\Windows\System32`
   - Restart your development environment

## Testing

To run the tests, use:
```bash
pytest
```