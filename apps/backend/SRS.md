# Software Requirements Specification (SRS)
## Anubis - AI Code Comparison & Evaluation System

### 1. Project Overview
**Project Name:** Anubis  
**Description:** A backend system that compares code generation across multiple AI models and evaluates outputs using standardized metrics.  
**Technology Stack:** Python, Google ADK (AI Development Kit)

---

### 2. System Purpose
Anubis takes a coding prompt, generates code using different AI models, and evaluates each output against predefined quality metrics to help users choose the best model for their needs.

---

### 3. Functional Requirements

#### 3.1 Input Processing
- **FR-1:** System shall accept a text prompt describing the coding task
- **FR-2:** System shall accept a list of AI model identifiers (e.g., "gemini-pro", "claude-3", "gpt-4")
- **FR-2.1:** System shall accept an optional ordered list of metrics for prioritized evaluation
- **FR-3:** System shall validate input prompt is non-empty
- **FR-4:** System shall validate at least one model is selected

#### 3.2 Code Generation
- **FR-5:** System shall send the prompt to each specified AI model via Google ADK
- **FR-5.1:** System shall include metric priorities in the generation prompt when provided
- **FR-5.2:** System shall instruct AI models to focus on higher-priority metrics using weighted importance
- **FR-6:** System shall retrieve generated code from each model
- **FR-7:** System shall handle API errors gracefully (timeout, rate limits, invalid responses)
- **FR-8:** System shall store generated code with model attribution

#### 3.3 Code Evaluation
The system shall evaluate each generated code sample against these metrics:

**FR-9: Readability (0-10 scale)**
- Variable naming quality
- Code structure and organization
- Presence of comments where needed

**FR-10: Consistency (0-10 scale)**
- Naming convention consistency
- Code style uniformity
- Pattern adherence

**FR-11: Time Complexity (0-10 scale)**
- Algorithm efficiency analysis
- Big O notation detection
- Performance optimization level

**FR-12: Code Documentation (0-10 scale)**
- Docstring presence and quality
- Inline comment adequacy
- Function/class documentation

**FR-13: External Dependencies (0-10 scale)**
- Number of dependencies (fewer is better)
- Dependency quality/reliability
- Standard library usage preference

**FR-14:** System shall calculate an overall code score as weighted average of all metrics
- **FR-14.1:** When metric priorities are provided, system shall use exponential decay weighting (decay rate 0.7)
- **FR-14.2:** Higher-ranked metrics shall receive exponentially higher weights
- **FR-14.3:** All weights shall be normalized to sum to 1.0
- **FR-14.4:** When no priorities are provided, system shall use default equal weights from config

#### 3.4 Output Generation
- **FR-15:** System shall return evaluation results in JSON format
- **FR-16:** System shall include individual metric scores for each model
- **FR-17:** System shall include overall score for each model
- **FR-18:** System shall include the generated code for each model
- **FR-19:** System shall rank models by overall score
- **FR-20:** System shall include best generated code in summary section

---

### 4. Input Schema
```json
{
  "prompt": "Write a function to find the longest palindromic substring",
  "models": ["gemini-pro", "gemini-flash", "claude-3-sonnet"],
  "metrics": ["time_complexity", "readability", "consistency", "code_documentation", "external_dependencies"]
}
```

**Field Specifications:**
- `prompt` (string, required): The coding task description
- `models` (array of strings, required): List of AI model identifiers to test
- `metrics` (array of strings, optional): Ordered list of metrics in descending priority order. Valid values: "readability", "consistency", "time_complexity", "code_documentation", "external_dependencies". When provided, higher-ranked metrics receive exponentially higher weights in scoring. If omitted, default equal weights are used.

---

### 5. Output Schema
```json
{
  "evaluation_id": "eval_abc123",
  "timestamp": "2025-11-15T14:30:00Z",
  "prompt": "Write a function to find the longest palindromic substring",
  "results": [
    {
      "model": "gemini-pro",
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
          "notes": "Standard DP approach"
        },
        "code_documentation": {
          "score": 8.0,
          "notes": "Good docstring, missing some inline comments"
        },
        "external_dependencies": {
          "score": 10.0,
          "dependencies_count": 0,
          "notes": "Uses only standard library"
        }
      },
      "execution_time_ms": 1250
    },
    {
      "model": "gemini-flash",
      "overall_score": 7.8,
      "generated_code": "def find_palindrome(text):\n    ...",
      "metrics": {
        "readability": { "score": 7.5, "notes": "..." },
        "consistency": { "score": 8.0, "notes": "..." },
        "time_complexity": { "score": 7.0, "detected_complexity": "O(n²)", "notes": "..." },
        "code_documentation": { "score": 6.5, "notes": "..." },
        "external_dependencies": { "score": 10.0, "dependencies_count": 0, "notes": "..." }
      },
      "execution_time_ms": 850
    }
  ],
  "ranking": [
    { "rank": 1, "model": "gemini-pro", "score": 8.4 },
    { "rank": 2, "model": "gemini-flash", "score": 7.8 }
  ],
  "summary": {
    "total_models_tested": 2,
    "successful_evaluations": 2,
    "failed_evaluations": 0,
    "best_model": "gemini-pro",
    "best_score": 8.4,
    "best_generated_code": "def longest_palindrome(s: str) -> str:\n    ..."
  }
}
```

---

### 6. Non-Functional Requirements

#### 6.1 Performance
- **NFR-1:** System shall process requests within 30 seconds for up to 3 models
- **NFR-2:** System shall support concurrent evaluation of multiple models

#### 6.2 Reliability
- **NFR-3:** System shall retry failed API calls up to 3 times
- **NFR-4:** System shall continue evaluation even if one model fails

#### 6.3 Maintainability
- **NFR-5:** Code shall follow PEP 8 style guidelines
- **NFR-6:** All functions shall have docstrings
- **NFR-7:** Configuration (API keys, model names) shall be externalized

#### 6.4 Security
- **NFR-8:** API keys shall be stored in environment variables
- **NFR-9:** Generated code shall be sanitized before storage

---

### 7. System Architecture

#### 7.1 Core Components

**CodeGenerator Module**
- Interfaces with Google ADK
- Manages API calls to different models
- Handles response parsing
- Builds dynamic prompts with metric priorities
- Instructs AI models on evaluation criteria importance

**CodeEvaluator Module**
- Implements metric evaluation logic
- Calculates scores for each metric
- Generates overall scores
- Computes dynamic weights based on metric priority order
- Applies exponential decay weighting algorithm

**MetricAnalyzers**
- ReadabilityAnalyzer: Evaluates code readability
- ConsistencyAnalyzer: Checks coding conventions
- ComplexityAnalyzer: Analyzes time/space complexity
- DocumentationAnalyzer: Assesses documentation quality
- DependencyAnalyzer: Counts and evaluates dependencies

**OutputFormatter Module**
- Structures evaluation results
- Generates JSON output
- Creates rankings
- Includes best generated code in summary

#### 7.2 Data Flow
1. Receive input (prompt + models + optional metrics priority)
2. Calculate dynamic weights if metrics priority provided
3. For each model:
   - Build prompt with metric priorities
   - Generate code via Google ADK with priority instructions
   - Store generated code
4. For each generated code:
   - Run all metric analyzers
   - Calculate individual scores
   - Calculate overall score using dynamic or default weights
5. Rank results by overall score
6. Format output including best generated code
7. Return JSON output

---

### 8. API Endpoints (if building REST API)

**POST /api/v1/evaluate**
- **Input:** JSON with prompt, models, and optional metrics priority array
- **Output:** Evaluation results JSON with weighted scoring and best generated code
- **Status Codes:** 200 (success), 400 (bad input), 500 (server error)

---

### 9. Configuration Requirements

**Environment Variables:**
```
GOOGLE_API_KEY=your_api_key_here
DEFAULT_MODELS=gemini-pro,gemini-flash
EVALUATION_TIMEOUT=30
MAX_RETRIES=3
```

**Config File (config.yaml):**
```yaml
metrics:
  weights:
    # Default weights (used when no priority order specified)
    readability: 0.25
    consistency: 0.20
    time_complexity: 0.25
    code_documentation: 0.15
    external_dependencies: 0.15

  # Exponential decay rate for priority-based weighting
  priority_decay_rate: 0.7

models:
  available:
    - gemini-pro
    - gemini-flash
    - gemini-ultra
```

---

### 10. Error Handling

- **ERR-1:** Invalid prompt → Return 400 with error message
- **ERR-2:** No models specified → Return 400 with error message
- **ERR-3:** API timeout → Retry up to 3 times, then mark as failed
- **ERR-4:** Invalid API response → Log error, continue with other models
- **ERR-5:** Code parsing error → Assign low scores, include error in notes

---

### 11. Testing Requirements

- **TEST-1:** Unit tests for each metric analyzer
- **TEST-2:** Integration tests for full evaluation pipeline
- **TEST-3:** Test cases with various code samples (simple, complex, buggy)
- **TEST-4:** Error handling tests (timeouts, invalid inputs)
- **TEST-5:** Performance tests with multiple models

---

### 12. Deliverables

1. **Python Package:** `anubis/`
   - `code_generator.py`
   - `evaluators/` (metric analyzers)
   - `output_formatter.py`
   - `main.py` (entry point)
   - `requirements.txt`
   - `config.yaml`

2. **Documentation:**
   - README.md with setup instructions
   - API documentation
   - Example usage

3. **Tests:**
   - `tests/` directory with unit and integration tests

---

### 13. Recent Updates (v1.1)

**Weighted Metrics Priority System:**
- Users can now specify metric priority order via `metrics` array in request
- Higher-ranked metrics receive exponentially higher weights (0.7 decay rate)
- AI models receive explicit instructions about metric priorities during generation
- Summary now includes the best generated code for easy access

**Example weighted scoring:**
For metrics order: `["time_complexity", "readability", "consistency", "code_documentation", "external_dependencies"]`
- time_complexity: ~33.7% weight
- readability: ~23.6% weight
- consistency: ~16.5% weight
- code_documentation: ~11.6% weight
- external_dependencies: ~8.1% weight

### 14. Future Enhancements (Out of Scope for Current Version)

- Web UI for visualization
- Database storage for historical comparisons
- Custom metric definitions
- Code execution and testing
- Multi-language support
- Model fine-tuning recommendations
- Configurable decay rate per request

---

### 14. Assumptions & Constraints

- Google ADK supports all specified models
- Generated code is valid Python
- Evaluation is static analysis only (no execution)
- User has valid Google API credentials
- Single-threaded evaluation per request

---

### 15. Glossary

- **ADK:** AI Development Kit
- **Metric:** A quantifiable measure of code quality
- **Overall Score:** Weighted average of all metric scores
- **Big O:** Time/space complexity notation
- **Metrics Priority:** User-defined order of metrics indicating relative importance
- **Exponential Decay Weighting:** Algorithm that assigns exponentially decreasing weights based on position
- **Decay Rate:** Factor (0.7) determining how quickly weights decrease for lower-priority metrics
- **Dynamic Weights:** Computed weights based on metrics priority order, as opposed to static config weights

---

**Document Version:** 1.1
**Last Updated:** November 15, 2025
**Author:** Anubis Team