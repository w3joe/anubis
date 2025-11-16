# Anubis ⚖️𓁣

**Automated AI Code Comparison & Evaluation System**

[![GitHub](https://img.shields.io/badge/GitHub-w3joe%2Fanubis-blue)](https://github.com/w3joe/anubis)

## 📖 Project Description

Anubis is an intelligent code evaluation platform that automates the process of comparing code generation across multiple AI models. Instead of manually testing different models and hoping for the best, Anubis takes a single prompt and automatically runs it through multiple AI models in parallel, evaluates each candidate using a comprehensive scoring pipeline, and surfaces the best result based on your priorities.

## 🎯 The Problem

Developers often face a frustrating workflow when using AI code generation:

1. **Manual Testing**: Developers try multiple AI models manually, one at a time
2. **Subjective Comparison**: Code quality is judged by eye, leading to inconsistent decisions
3. **Uncertainty**: No objective metrics to determine which model produces the best code for a specific task
4. **No Priority System**: Can't easily prioritize what matters most (e.g., performance vs. readability)

This process is slow, inconsistent, and doesn't scale.

## ✨ The Solution

Anubis automates the entire workflow:

1. **Parallel Multi-Model Generation**: Takes a single prompt and runs it through multiple AI models simultaneously in different branches
2. **Automated Evaluation**: Each code candidate is automatically evaluated using a comprehensive scoring pipeline
3. **Priority-Based Weighting**: Metrics are weighted according to user-selected priorities (e.g., if performance matters most, time complexity gets higher weight)
4. **Objective Ranking**: Produces a final weighted score for each generated code and ranks them objectively
5. **Best Code Surface**: Automatically surfaces the best code based on your priorities

https://github.com/user-attachments/assets/b94d51f0-d8a7-42d3-9ebe-23efdf90fc99

**Result**: Fast, consistent, and objective code comparison that scales.

## 🏗️ Architecture

Anubis follows a modular, agentic architecture with clear separation of concerns:

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (Next.js)                     │
│              User Interface & Real-time Streaming           │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ HTTP/SSE
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend API (Flask)                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Code Generator (Coding Agent)                │   │
│  │  • Multi-model parallel code generation              │   │
│  │  • Google AI SDK integration                         │   │
│  │  • Streaming support                                 │   │
│  └───────────────────┬──────────────────────────────────┘   │
│                      │                                      │
│                      ▼                                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │      Code Evaluator (Evaluator Agent)                │   │
│  │  • Orchestrates metric evaluation                    │   │
│  │  • Dynamic weight calculation                        │   │
│  │  • Overall score computation                         │   │
│  └───────────────────┬──────────────────────────────────┘   │
│                      │                                      │
│                      ▼                                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Metric Analyzers                        │   │
│  │  • ReadabilityAnalyzer                               │   │
│  │  • ConsistencyAnalyzer                               │   │
│  │  • ComplexityAnalyzer                                │   │
│  │  • DocumentationAnalyzer                             │   │
│  │  • DependencyAnalyzer                                │   │
│  └───────────────────┬──────────────────────────────────┘   │
│                      │                                      │
│                      ▼                                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Output Formatter                           │   │
│  │  • JSON structure generation                         │   │
│  │  • Ranking computation                               │   │
│  │  • Summary creation                                  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                        │
                        │
                        ▼
            ┌───────────────────────┐
            │   Google AI Studio    │
            │   Gemini Models       │
            └───────────────────────┘
```

### Data Flow

1. **Input Processing**: User provides prompt, model list, and optional metric priorities
2. **Dynamic Weight Calculation**: If priorities provided, calculate exponential decay weights
3. **Parallel Code Generation**: 
   - Build prompts with metric priority instructions
   - Generate code via Google AI SDK for each model simultaneously
   - Stream results in real-time (SSE endpoint)
4. **Code Evaluation**:
   - Run all metric analyzers on each generated code
   - Calculate individual metric scores
   - Compute overall weighted score
5. **Ranking & Output**:
   - Rank models by overall score
   - Format results with best code highlighted
   - Return JSON or stream via SSE

### Technology Stack

**Backend:**
- Python 3.12+
- Flask - Web framework
- Google AI SDK (genai) - Gemini API integration
- PyYAML - Configuration management

**Frontend:**
- Next.js 16+ - React framework
- TypeScript - Type safety
- Server-Sent Events (SSE) - Real-time streaming

**Infrastructure:**
- Turborepo - Monorepo management
- pnpm - Package manager

## 🤖 Google AI Studio & Gemini Integration

Anubis leverages Google AI Studio and Gemini models as core components of its agentic workflow:

### How We Use Google AI Studio

1. **Prompt Design & Testing**: We designed and tested our prompt templates inside Google AI Studio to optimize output quality across different Gemini variants
2. **Rapid Iteration**: Google AI Studio enabled quick iteration on:
   - System instructions for code generation
   - Code-generation prompts
   - Scoring heuristics and evaluation criteria
3. **Model Selection**: Tested various Gemini models (gemini-2.0-flash-exp, gemini-1.5-pro, gemini-1.5-flash) to understand their strengths

### Gemini Models in the Pipeline

Gemini models serve as one of the core "branches" in our multi-model AB testing pipeline:

- **Comparator Agent**: Uses Gemini models via Google AI SDK to generate code candidates
- **Streaming Support**: Real-time code generation with Server-Sent Events
- **Multi-Model Comparison**: Gemini variants are compared against each other and other models
- **Priority-Aware Generation**: Prompts include metric priorities to guide Gemini's code generation focus

### Integration Details

- **SDK**: Google AI SDK (`google.genai`) for programmatic access
- **Streaming**: Real-time streaming of code chunks as they're generated
- **Error Handling**: Robust retry logic and graceful degradation
- **Performance**: Parallel execution of multiple Gemini model variants

## 🚀 Features

### Core Features

- ✅ **Multi-Model Code Generation**: Generate code from multiple AI models simultaneously
- ✅ **Real-Time Streaming**: Watch code generation happen in real-time via Server-Sent Events
- ✅ **Comprehensive Evaluation**: 5 key metrics with detailed analysis:
  - **Readability**: Variable naming, structure, comments
  - **Consistency**: Naming conventions, code style uniformity
  - **Time Complexity**: Algorithm efficiency, Big O analysis
  - **Code Documentation**: Docstrings, inline comments
  - **External Dependencies**: Standard library preference
- ✅ **Priority-Based Weighting**: Customize metric importance with exponential decay weighting
- ✅ **Automated Ranking**: Objective ranking by weighted overall score
- ✅ **Best Code Surface**: Automatically highlights the best generated code
- ✅ **RESTful API**: Easy-to-use JSON API endpoints
- ✅ **Streaming API**: Real-time updates via Server-Sent Events

### Advanced Features

- **Parallel Execution**: Multiple models generate code simultaneously, significantly reducing total time
- **Dynamic Weighting**: Exponential decay algorithm for priority-based metric weighting
- **Graceful Error Handling**: Continues evaluation even if one model fails
- **Retry Logic**: Automatic retries for failed API calls
- **Configurable**: YAML-based configuration for weights and models

## 📦 Project Structure

```
anubis/
├── apps/
│   ├── backend/              # Python Flask backend
│   │   ├── anubis/          # Core Anubis package
│   │   │   ├── code_generator.py      # Code generation via Google AI SDK
│   │   │   ├── code_evaluator.py      # Orchestrates metric evaluation
│   │   │   ├── output_formatter.py    # Formats results to JSON
│   │   │   └── evaluators/            # Metric analyzers
│   │   │       ├── base_analyzer.py
│   │   │       ├── readability_analyzer.py
│   │   │       ├── consistency_analyzer.py
│   │   │       ├── complexity_analyzer.py
│   │   │       ├── documentation_analyzer.py
│   │   │       └── dependency_analyzer.py
│   │   ├── app.py           # Flask application
│   │   ├── config.yaml      # Configuration
│   │   └── requirements.txt  # Python dependencies
│   │
│   └── web/                 # Next.js frontend
│       ├── app/             # Next.js app directory
│       └── package.json
│
├── packages/                # Shared packages
│   ├── ui/                 # Shared UI components
│   ├── eslint-config/      # ESLint configuration
│   └── typescript-config/  # TypeScript configuration
│
├── package.json            # Root package.json (Turborepo)
└── turbo.json              # Turborepo configuration
```

## 🛠️ Setup

### Prerequisites

- Node.js 18+ and pnpm 9.0.0+
- Python 3.12+
- Google API Key ([Get one here](https://aistudio.google.com/apikey))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/w3joe/anubis.git
   cd anubis
   ```

2. **Install dependencies:**
   ```bash
   pnpm install
   ```

3. **Set up backend:**
   ```bash
   cd apps/backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   # In apps/backend/
   export GOOGLE_API_KEY=your_api_key_here
   # Or create a .env file
   ```

5. **Run the development servers:**
   ```bash
   # From project root
   pnpm run dev
   ```

   This will start:
   - Backend API at `http://localhost:5001`
   - Frontend at `http://localhost:3000`

## 📡 API Endpoints

### 1. Health Check
```http
GET /health
```

### 2. Code Evaluation (Main Endpoint)
```http
POST /api/v1/evaluate
Content-Type: application/json
```

**Request:**
```json
{
  "prompt": "Write a function to find the longest palindromic substring",
  "models": ["gemini-2.0-flash-exp", "gemini-1.5-pro"],
  "metrics": ["time_complexity", "readability", "consistency"]
}
```

**Response:** See [Backend README](apps/backend/README.md) for full response schema.

### 3. Streaming Evaluation
```http
POST /api/v1/evaluate/stream
Content-Type: application/json
```

**Request:** Same as above

**Response:** Server-Sent Events stream with real-time updates:
- `generation_start`: Model begins generating
- `code_chunk`: Incremental code chunks
- `generation_complete`: Model finished
- `evaluation_result`: Metrics and scores
- `summary`: Final summary with rankings
- `complete`: Stream finished

## 📊 Evaluation Metrics

Each metric is scored on a 0-10 scale:

| Metric | Description | What It Measures |
|--------|-------------|-------------------|
| **Readability** | Code clarity and maintainability | Variable naming, structure, comments |
| **Consistency** | Code style uniformity | Naming conventions, pattern adherence |
| **Time Complexity** | Algorithm efficiency | Big O notation, performance optimization |
| **Code Documentation** | Documentation quality | Docstrings, inline comments |
| **External Dependencies** | Dependency management | Standard library usage, dependency count |

### Priority-Based Weighting

When you provide a metrics array, Anubis uses exponential decay weighting:
- Higher-ranked metrics get exponentially higher weights
- Weights are normalized to sum to 1.0
- Example: `["time_complexity", "readability"]` gives time_complexity ~70% weight, readability ~30%

## 🎬 Example Usage

### Using cURL

```bash
curl -X POST http://localhost:5000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a binary search function",
    "models": ["gemini-2.0-flash-exp", "gemini-1.5-pro"],
    "metrics": ["time_complexity", "readability"]
  }'
```

### Using the Frontend

1. Navigate to `http://localhost:3000`
2. Enter your coding prompt
3. Select models to compare
4. Optionally set metric priorities
5. Click "Evaluate" and watch real-time results

## 🧪 Development

### Running Tests

```bash
cd apps/backend
pytest tests/
```

### Code Style

- **Backend**: Follows PEP 8 style guidelines
- **Frontend**: ESLint + Prettier configured

### Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 📝 License

[Add your license here]

## 🔗 Links

- **GitHub Repository**: https://github.com/w3joe/anubis
- **Google AI Studio**: https://aistudio.google.com
- **Gemini API Docs**: https://ai.google.dev/docs

---

**Anubis** - Weighing the code of the AI gods ⚖️

*Automated. Objective. Fast.*
