# GiftSnapGiftingAI Backend

A FastAPI-based backend for GiftSnapGiftingAI, providing intelligent gift recommendations using the LLaMA 3 70B model via Groq's API.

## Features

- 🎁 AI-powered personalized gift recommendations
- 🚀 Fast and scalable FastAPI backend
- 🔒 Secure API key management with environment variables
- 📝 Interactive API documentation with Swagger UI
- 🤖 Powered by LLaMA 3 70B model

## Prerequisites

- Python 3.8+
- Groq API key (Get one from [Groq](https://console.groq.com/))

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/GiftSnapGiftingAIBackend.git
   cd GiftSnapGiftingAIBackend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file and add your Groq API key:
   ```env
   GIFTSNAP_API_KEY=your_groq_api_key_here
   ```

## Usage

1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

2. Access the API:
   - Interactive API docs: http://localhost:8000/docs
   - Direct API endpoint: `GET` or `POST` to `http://localhost:8000/generate?prompt=your_prompt_here`

### Example Request

```bash
curl "http://localhost:8000/generate?prompt=I need a birthday gift for my mom who loves gardening"
```

### Example Response

```json
{
  "response": "Here are some thoughtful gift ideas for your mom who loves gardening..."
}
```

## API Endpoints

- `GET /generate` - Generate gift recommendations based on the provided prompt
- `POST /generate` - Same as GET, but accepts the prompt in the request body

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GIFTSNAP_API_KEY` | Yes | Your Groq API key |
| `LOG_LEVEL` | No | Logging level (default: INFO) |

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Groq](https://groq.com/)
- [LLaMA 3](https://ai.meta.com/llama/)
