# Voice Biometrics API

A FastAPI-based voice biometrics system that provides speaker enrollment and verification capabilities using voice embeddings and similarity matching.

## Features

- **Voice Enrollment**: Register users with their voice samples
- **Voice Verification**: Verify speaker identity using voice similarity
- **Liveness Detection**: Generate random phrases for anti-spoofing
- **Secure Storage**: Encrypted storage of voice embeddings
- **RESTful API**: Clean, documented API endpoints
- **Database Integration**: PostgreSQL support with SQLAlchemy ORM

## Tech Stack

- **Backend**: FastAPI (Python)
- **Voice Processing**: Resemblyzer, SoundFile
- **Database**: PostgreSQL with SQLAlchemy
- **Encryption**: Cryptography library
- **Server**: Uvicorn with hot reload

## Project Structure

```
VoiceBiometrics/
├── app/
│   ├── db/
│   │   ├── database.py      # Database configuration
│   │   ├── models.py        # SQLAlchemy models
│   │   └── mock_db.py       # In-memory storage (fallback)
│   ├── routes/
│   │   ├── auth_routes.py   # Voice enrollment/verification endpoints
│   │   └── phrase_routes.py # Liveness detection endpoints
│   └── services/
│       ├── voice_service.py     # Voice embedding extraction
│       └── encryption_service.py # Data encryption utilities
├── db_scripts/              # Database setup scripts
├── alembic/                 # Database migrations
├── main.py                  # FastAPI application entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL database
- Virtual environment (recommended)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd VoiceBiometrics
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/voicebiometrics
   FERNET_KEY=your-secret-key-here
   ```
⚠️ **Important**: Do NOT regenerate the `FERNET_KEY` once users are enrolled. Changing it will break decryption for stored embeddings.

5. **Initialize database**  
   ```bash
   # Run database scripts
   python db_scripts/run_db_scripts.py
   
   # Or use Alembic for migrations
   alembic upgrade head
   ```

## Usage

### Starting the Server

```bash
# Development mode with auto-reload
uvicorn main:app --reload

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, you can access:
- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`
- **OpenAPI schema**: `http://localhost:8000/openapi.json`

## API Endpoints

### Authentication Routes

#### Enroll Voice
```http
POST /auth/enroll/{user_id}
Content-Type: multipart/form-data

file: [WAV audio file]
```

**Response:**
```json
{
  "message": "Voice enrolled successfully for user: {user_id}"
}
```

#### Verify Voice
```http
POST /auth/verify/{user_id}
Content-Type: multipart/form-data

file: [WAV audio file]
```

**Response:**
```json
{
  "verified": true,
  "voice_similarity": 0.92
}
```

### Liveness Detection

#### Generate Phrase
```http
GET /phrase/generate
```

**Response:**
```json
{
  "phrase": "Green apples are sweet"
}
```

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "ok"
}
```

## Usage Examples

### Python Client Example

```python
import requests

# Enroll a user
with open('user_voice.wav', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/auth/enroll/user123', files=files)
    print(response.json())

# Verify a user
with open('test_voice.wav', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/auth/verify/user123', files=files)
    result = response.json()
    print(f"Verified: {result['verified']}")
    print(f"Similarity: {result['voice_similarity']}")

# Get liveness phrase
response = requests.get('http://localhost:8000/phrase/generate')
phrase = response.json()['phrase']
print(f"Say this phrase: {phrase}")
```

### cURL Examples

```bash
# Enroll voice
curl -X POST "http://localhost:8000/auth/enroll/user123" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@voice_sample.wav"

# Verify voice
curl -X POST "http://localhost:8000/auth/verify/user123" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_voice.wav"

# Get liveness phrase
curl -X GET "http://localhost:8000/phrase/generate"
```

## Configuration

### Voice Verification Settings

- **Similarity Threshold**: 0.85 (configurable in `auth_routes.py`)
- **Supported Audio Format**: WAV files only
- **Embedding Model**: Resemblyzer VoiceEncoder

### Database Configuration

The application supports both PostgreSQL (production) and in-memory storage (development). Configure via `DATABASE_URL` environment variable.

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Code Style

```bash
# Install formatting tools
pip install black isort

# Format code
black .
isort .
```

## Security Considerations

- Voice embeddings are encrypted before storage
- Only WAV files are accepted to prevent malicious uploads
- Similarity threshold prevents false positives
- Liveness detection helps prevent replay attacks

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify PostgreSQL is running
   - Check `DATABASE_URL` in `.env` file
   - Ensure database exists

2. **Audio Processing Error**
   - Ensure audio file is in WAV format
   - Check file size (should be reasonable)
   - Verify audio quality (clear speech)

3. **Import Errors**
   - Activate virtual environment
   - Reinstall dependencies: `pip install -r requirements.txt`

### Logs

Check server logs for detailed error information:
```bash
uvicorn main:app --reload --log-level debug
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
- Create an issue in the repository
- Contact: [your-email@example.com] 