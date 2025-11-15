# Anubis - AI Code Comparison & Evaluation System

Anubis is a backend system that compares code generation across multiple AI models and evaluates outputs using standardized metrics. It helps developers choose the best AI model for their coding tasks.

## Features

- **Multi-Model Code Generation**: Generate code from multiple AI models simultaneously
- **Comprehensive Evaluation**: Evaluate code based on 5 key metrics:
  - Readability (variable naming, structure, comments)
  - Consistency (naming conventions, code style)
  - Time Complexity (algorithm efficiency)
  - Code Documentation (docstrings, inline comments)
  - External Dependencies (standard library usage)
- **Automated Ranking**: Rank models by overall score
- **RESTful API**: Easy-to-use JSON API endpoints

## Project Structure

```
apps/backend/
├── anubis/                    # Core Anubis package
│   ├── __init__.py
│   ├── code_generator.py      # Code generation via Google ADK
│   ├── code_evaluator.py      # Orchestrates metric evaluation
│   ├── output_formatter.py    # Formats results to JSON
│   └── evaluators/            # Metric analyzers
│       ├── __init__.py
│       ├── base_analyzer.py
│       ├── readability_analyzer.py
│       ├── consistency_analyzer.py
│       ├── complexity_analyzer.py
│       ├── documentation_analyzer.py
│       └── dependency_analyzer.py
├── tests/                     # Unit and integration tests
├── app.py                     # Flask application
├── config.yaml                # Configuration file
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Setup

### Prerequisites

- Python 3.12+
- Google API Key ([Get one here](https://aistudio.google.com/apikey))

### Installation

1. **Clone the repository and navigate to the backend directory:**
   ```bash
   cd apps/backend
   ```

2. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your Google API key:
   # GOOGLE_API_KEY=your_actual_api_key_here
   ```

5. **Run the application:**
   ```bash
   export $(cat .env | xargs)
   python app.py
   ```

   The server will start at `http://localhost:5000`

## API Endpoints

### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

### 2. Code Evaluation (Main Endpoint)
```http
POST /api/v1/evaluate
Content-Type: application/json
```

**Request Body:**
```json
{
  "prompt": "Write a function to find the longest palindromic substring",
  "models": ["gemini-2.0-flash-exp", "gemini-2.5-pro", "gemini-2.0-flash"]
}
```

**Response:**
```json
{
  "evaluation_id": "eval_abc123",
  "timestamp": "2025-11-15T14:30:00Z",
  "prompt": "Write a function to find the longest palindromic substring",
  "results": [
    {
      "model": "gemini-2.0-flash-exp",
      "overall_score": 8.4,
      "generated_code": "def longest_palindrome(s: str) -> str:\n    ...",
      "metrics": {
        "readability": {
          "score": 8.5,
          "notes": "Clear variable names, well-structured"
        },
        "consistency": {
          "score": 9.0,
          "notes": "Consistent naming conventions"
        },
        "time_complexity": {
          "score": 7.5,
          "detected_complexity": "O(n²)",
          "notes": "Quadratic time - acceptable for small inputs"
        },
        "code_documentation": {
          "score": 8.0,
          "notes": "Good docstrings, appropriate inline comments"
        },
        "external_dependencies": {
          "score": 10.0,
          "dependencies_count": 0,
          "notes": "Uses only standard library"
        }
      },
      "execution_time_ms": 1250,
      "success": true,
      "error": null
    }
  ],
  "ranking": [
    { "rank": 1, "model": "gemini-2.0-flash-exp", "score": 8.4 },
    { "rank": 2, "model": "gemini-2.0-flash", "score": 7.8 }
  ],
  "summary": {
    "total_models_tested": 2,
    "successful_evaluations": 2,
    "failed_evaluations": 0,
    "best_model": "gemini-2.0-flash-exp",
    "best_score": 8.4
  }
}
```

### 3. Simple Text Generation
```http
POST /api/gemini/generate
Content-Type: application/json
```

**Request Body:**
```json
{
  "prompt": "Explain quantum computing in simple terms",
  "model": "gemini-2.0-flash-exp"
}
```

### 4. Chat with Gemini
```http
POST /api/gemini/chat
Content-Type: application/json
```

**Request Body:**
```json
{
  "messages": [
    {"role": "user", "content": "What is Python?"},
    {"role": "model", "content": "Python is a programming language..."},
    {"role": "user", "content": "What are its main features?"}
  ],
  "model": "gemini-2.0-flash-exp"
}
```

## Configuration

Edit `config.yaml` to customize metric weights and available models:

```yaml
metrics:
  weights:
    readability: 0.25
    consistency: 0.20
    time_complexity: 0.25
    code_documentation: 0.15
    external_dependencies: 0.15

models:
  available:
    - gemini-2.0-flash-exp
    - gemini-2.5-pro
    - gemini-2.0-flash

evaluation:
  timeout: 30
  max_retries: 3
```

## Evaluation Metrics

### Readability (0-10)
- Variable naming quality
- Code structure and organization
- Presence of comments where needed

### Consistency (0-10)
- Naming convention consistency (snake_case vs camelCase)
- Code style uniformity
- Pattern adherence

### Time Complexity (0-10)
- Algorithm efficiency analysis
- Big O notation detection
- Performance optimization level

### Code Documentation (0-10)
- Docstring presence and quality
- Inline comment adequacy
- Function/class documentation

### External Dependencies (0-10)
- Number of dependencies (fewer is better)
- Dependency quality/reliability
- Standard library usage preference

## Example Usage

```bash
curl -X POST http://localhost:5000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a binary search function",
    "models": ["gemini-2.0-flash-exp", "gemini-2.0-flash"]
  }'
```

## Development

### Running Tests
```bash
# Coming soon
pytest tests/
```

### Code Style
This project follows PEP 8 style guidelines. All functions include docstrings.

## Error Handling

- **400 Bad Request**: Invalid input (missing prompt or models)
- **500 Internal Server Error**: Server-side error (check logs)

Failed model evaluations are handled gracefully and continue with other models.

## Technology Stack

- **Python 3.12+**
- **Flask** - Web framework
- **Google ADK** - AI model access
- **Google Genai** - Gemini API
- **PyYAML** - Configuration management

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Support

For issues and questions, please open an issue in the repository.

---

**Anubis** - Weighing the code of the AI gods ⚖️
