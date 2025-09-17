# Roblox-Outfit-Marketplace-backend
Backend service that powers chat and outfit selection in our Roblox game "Ai-Style-Assistant", using AI agents and the Roblox catalog.

## Features

- **Chat Endpoint** (`/chat`): NPC chat system that responds to user prompts with style advice
- **Recommendation Endpoint** (`/recommend`): Fetches 6-10 outfit items from Roblox catalog by theme
- **FastAPI Backend**: Modern, fast web framework with automatic API documentation
- **Pydantic Models**: Type validation and serialization for all data
- **CORS Support**: Cross-origin requests enabled for web integration

## API Endpoints

### POST /chat
Chat with the AI Style Assistant NPC.

**Request:**
```json
{
  "message": "Hello! I need style advice"
}
```

**Response:**
```json
{
  "reply": "Welcome to the Roblox Outfit Marketplace! I'm here to help you find the perfect style!"
}
```

### POST /recommend
Get outfit recommendations by theme.

**Request:**
```json
{
  "theme": "casual"
}
```

**Response:**
```json
{
  "items": [
    {
      "assetId": 1234567890,
      "type": "shirt"
    },
    {
      "assetId": 2345678901,
      "type": "pants"
    }
  ]
}
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Rushabh-Runwal/Roblox-Outfit-Marketplace-backend.git
cd Roblox-Outfit-Marketplace-backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python server/main.py
```

Or using uvicorn directly:
```bash
uvicorn server.main:app --reload --host 0.0.0.0 --port 8000
```

## Usage

The server will start on `http://localhost:8000`

- **API Documentation**: Visit `http://localhost:8000/docs` for interactive Swagger UI
- **Alternative Docs**: Visit `http://localhost:8000/redoc` for ReDoc documentation

## Supported Themes

The recommendation system supports various themes:
- `casual` - Everyday comfortable clothing
- `formal` - Professional and elegant attire
- `sporty` - Athletic and active wear
- `gothic` - Dark and alternative fashion
- `kawaii` - Cute and colorful Japanese-inspired styles

## Technical Details

- **Framework**: FastAPI with uvicorn ASGI server
- **HTTP Client**: httpx for async HTTP requests
- **Validation**: Pydantic for data models and validation
- **CORS**: Enabled for cross-origin requests
- **Logging**: Structured logging for debugging and monitoring

## Development

To run in development mode with auto-reload:
```bash
uvicorn server.main:app --reload
```

The API automatically generates OpenAPI documentation available at `/docs` and `/redoc` endpoints.
