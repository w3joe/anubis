# Anubis API - Curl Examples

This document contains curl command examples for testing all Anubis API endpoints.

## Prerequisites

Make sure the Flask server is running:
```bash
cd apps/backend
export GOOGLE_API_KEY=your_api_key_here
python app.py
```

The server will be available at `http://localhost:5000`

---

## 1. Health Check

Check if the API is running:

```bash
curl http://localhost:5000/health
```

**Expected Response:**
```json
{
  "status": "healthy"
}
```

---

## 2. Root Endpoint

Get welcome message:

```bash
curl http://localhost:5000/
```

**Expected Response:**
```json
{
  "message": "Hello from Anubis Backend!"
}
```

---

## 3. Simple Text Generation (Gemini)

Generate text using Google Gemini:

```bash
curl -X POST http://localhost:5000/api/gemini/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain what a binary search tree is in 2 sentences",
    "model": "gemini-2.0-flash-exp"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "response": "A binary search tree is a hierarchical data structure...",
  "model": "gemini-2.0-flash-exp"
}
```

---

## 4. Chat with Gemini

Multi-turn conversation:

```bash
curl -X POST http://localhost:5000/api/gemini/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is recursion?"},
      {"role": "model", "content": "Recursion is when a function calls itself."},
      {"role": "user", "content": "Give me a simple example"}
    ],
    "model": "gemini-2.0-flash-exp"
  }'
```

---

## 5. Main Anubis Evaluation (Single Model)

Evaluate code generation from one AI model:

```bash
curl -X POST http://localhost:5000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function to calculate factorial with recursion",
    "models": ["gemini-2.0-flash-exp"]
  }'
```

**Response includes:**
- Generated code
- Metrics scores (readability, consistency, complexity, documentation, dependencies)
- Overall score
- Execution time

---

## 6. Main Anubis Evaluation (Multiple Models)

Compare code generation across multiple AI models:

```bash
curl -X POST http://localhost:5000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a binary search function in Python with proper documentation and error handling",
    "models": ["gemini-2.0-flash-exp", "gemini-2.5-pro", "gemini-2.0-flash"]
  }'
```

**Formatted output (with jq):**
```bash
curl -X POST http://localhost:5000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a function to find the longest palindromic substring",
    "models": ["gemini-2.0-flash-exp", "gemini-2.0-flash"]
  }' | jq '.'
```

---

## 7. Complex Example - Sorting Algorithm Comparison

Compare how different models implement a sorting algorithm:

```bash
curl -X POST http://localhost:5000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Implement quicksort in Python with: 1) Clear docstrings, 2) Type hints, 3) Edge case handling, 4) In-place sorting",
    "models": ["gemini-2.0-flash-exp", "gemini-2.5-pro", "gemini-2.0-flash"]
  }' | jq '{
    evaluation_id,
    prompt,
    ranking,
    summary,
    top_result: .results[0] | {
      model,
      overall_score,
      metrics: {
        readability: .metrics.readability.score,
        complexity: .metrics.time_complexity.detected_complexity,
        documentation: .metrics.code_documentation.score
      }
    }
  }'
```

---

## 8. Save Response to File

Save the full evaluation results:

```bash
curl -X POST http://localhost:5000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a LRU cache implementation in Python",
    "models": ["gemini-2.0-flash-exp", "gemini-2.0-flash"]
  }' | jq '.' > evaluation_results.json
```

Then view specific parts:

```bash
# View ranking
jq '.ranking' evaluation_results.json

# View best model's code
jq '.results[0].generated_code' evaluation_results.json

# View all metrics for first result
jq '.results[0].metrics' evaluation_results.json
```

---

## Error Handling Examples

### Missing Prompt

```bash
curl -X POST http://localhost:5000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "models": ["gemini-2.0-flash-exp"]
  }'
```

**Response:**
```json
{
  "error": "Missing prompt in request body"
}
```

### Missing Models

```bash
curl -X POST http://localhost:5000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a function"
  }'
```

**Response:**
```json
{
  "error": "At least one model must be specified"
}
```

### Empty Prompt

```bash
curl -X POST http://localhost:5000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "   ",
    "models": ["gemini-2.0-flash-exp"]
  }'
```

**Response:**
```json
{
  "error": "Prompt cannot be empty"
}
```

---

## Using Environment Variables

Save common values:

```bash
export API_URL="http://localhost:5000"
export DEFAULT_MODEL="gemini-2.0-flash-exp"

curl -X POST $API_URL/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d "{
    \"prompt\": \"Write a fibonacci function\",
    \"models\": [\"$DEFAULT_MODEL\"]
  }"
```

---

## Performance Testing

Test with timing information:

```bash
time curl -X POST http://localhost:5000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a merge sort function",
    "models": ["gemini-2.0-flash-exp"]
  }' | jq '.summary'
```

---

## Automated Testing

Run all tests:

```bash
./test_api.sh
```

Quick single test:

```bash
./quick_test.sh
```

---

## Tips

1. **Install jq** for better JSON formatting:
   ```bash
   brew install jq  # macOS
   apt-get install jq  # Ubuntu/Debian
   ```

2. **Pretty print responses**:
   ```bash
   curl ... | jq '.'
   ```

3. **Extract specific fields**:
   ```bash
   curl ... | jq '.ranking'
   curl ... | jq '.summary.best_model'
   ```

4. **Check HTTP status codes**:
   ```bash
   curl -w "\nHTTP Status: %{http_code}\n" ...
   ```

5. **Verbose output** for debugging:
   ```bash
   curl -v ...
   ```
