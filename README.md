# Roblox-Outfit-Marketplace-backend
Backend service that powers chat and outfit selection in our Roblox game "Ai-Style-Assistant", using AI agents and the Roblox catalog.

## Features

- **Chat Endpoint** (`/chat`): NPC chat system that responds to user prompts with style advice
  - Input: `{ "prompt": string, "user_id": int }`
  - Output: `{ "success": true, "user_id": int, "reply": string }`
- **Recommendation Endpoint** (`/recommend`): Fetches 6-10 outfit items from Roblox catalog by theme
  - Input: `{ "theme": string, "user_id": int }`
  - Fetches items from `https://catalog.roblox.com/v2/search/items/details`
  - Output: `{ "success": true, "user_id": int, "message": string, "outfit": [{"assetId": string, "type": string}] }`
- **FastAPI Backend**: Modern, fast web framework with automatic API documentation
- **Pydantic Models**: Type validation and serialization for all data
- **CORS Support**: Cross-origin requests enabled for web integration
- **Error Handling**: Proper 502 responses for external API failures with fallback data
- **Retry Logic**: 3-attempt retry with timeout for Roblox API calls

## API Endpoints

### POST /chat
Chat with the AI Style Assistant NPC.

**Request:**
```json
{
  "prompt": "I want a knight outfit.",
  "user_id": 7470350941
}
```

**Response:**
```json
{
  "success": true,
  "user_id": 7470350941,
  "reply": "Welcome to the Roblox Outfit Marketplace! I'm here to help you find the perfect style!"
}
```

### POST /recommend
Get outfit recommendations by theme from the Roblox catalog.

**Request:**
```json
{
  "theme": "knight",
  "user_id": 7470350941
}
```

**Response:**
```json
{
  "success": true,
  "user_id": 7470350941,
  "message": "Your knight outfit is ready!",
  "outfit": [
    {
      "assetId": "123",
      "type": "Accessory"
    },
    {
      "assetId": "456",
      "type": "Hat"
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

### Example cURL Commands

Test the chat endpoint:
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "I want a knight outfit.", "user_id": 7470350941}'
```

Test the recommend endpoint:
```bash
curl -X POST "http://localhost:8000/recommend" \
  -H "Content-Type: application/json" \
  -d '{"theme": "knight", "user_id": 7470350941}'
```

## Supported Themes

The recommendation system supports various themes:
- `casual` - Everyday comfortable clothing
- `formal` - Professional and elegant attire
- `sporty` - Athletic and active wear
- `gothic` - Dark and alternative fashion
- `kawaii` - Cute and colorful Japanese-inspired styles

## Technical Details

- **Framework**: FastAPI with uvicorn ASGI server
- **HTTP Client**: httpx for async HTTP requests with timeout and retry logic
- **Validation**: Pydantic for data models and validation
- **CORS**: Enabled for cross-origin requests (allow localhost:PORT)
- **Logging**: Structured logging for debugging and monitoring
- **API Integration**: Roblox Catalog v2 API (`/search/items/details`) with `categoryFilter=CommunityCreations`
- **Retry Logic**: 3 attempts with 10-second timeout for external API calls
- **Fallback**: Sample data when external API is unavailable

## Development

To run in development mode with auto-reload:
```bash
uvicorn server.main:app --reload
```

The API automatically generates OpenAPI documentation available at `/docs` and `/redoc` endpoints.
