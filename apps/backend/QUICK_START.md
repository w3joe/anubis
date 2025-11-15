# Anubis - Quick Start Guide

## ✅ Fixed Issues

The API is now working correctly with updated model names:
- ✅ Server running on **port 5001** (avoiding macOS AirPlay on port 5000)
- ✅ Using correct Gemini 2.x model names
- ❌ Old models (`gemini-1.5-pro`, `gemini-1.5-flash`) are **no longer available**

## 🚀 Start the Server

```bash
cd /Users/w3joe/Documents/projects/anubis/apps/backend

# Make sure virtual environment is activated
source .venv/bin/activate

# Set your API key
export GOOGLE_API_KEY=your_api_key_here

# Start the server (will run on port 5001)
python app.py
```

The server will be available at: **http://localhost:5001**

## ✅ Working Model Names

Use these model names in your requests:

### Recommended Models
- `gemini-2.0-flash-exp` ⭐ (fastest, experimental)
- `gemini-2.0-flash` (stable)
- `gemini-2.5-flash` (newer, faster)
- `gemini-2.5-pro` (more capable)

### Latest Aliases
- `gemini-flash-latest`
- `gemini-pro-latest`

## 📝 Working Examples

### Single Model Test
```bash
curl -X POST http://localhost:5001/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function to check if a number is prime",
    "models": ["gemini-2.0-flash-exp"]
  }' | jq '.'
```

### Compare Two Models
```bash
curl -X POST http://localhost:5001/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a binary search function with proper documentation",
    "models": ["gemini-2.0-flash-exp", "gemini-2.0-flash"]
  }' | jq '.ranking'
```

### Compare Three Models
```bash
curl -X POST http://localhost:5001/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Implement quicksort in Python with type hints",
    "models": ["gemini-2.0-flash-exp", "gemini-2.5-flash", "gemini-2.5-pro"]
  }' | jq '{ranking, summary}'
```

## 🎬 Run Test Scripts

### Quick Test (Single Example)
```bash
./quick_test.sh
```

### Working Examples (Multiple Tests)
```bash
./working_examples.sh
```

### Full Test Suite
```bash
./test_api.sh
```

## 📊 View Results

### See Rankings Only
```bash
curl -X POST http://localhost:5001/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a function to find palindromes",
    "models": ["gemini-2.0-flash-exp", "gemini-2.0-flash"]
  }' | jq '.ranking'
```

### See Summary Only
```bash
curl ... | jq '.summary'
```

### See Generated Code from Winner
```bash
curl ... | jq '.results[0].generated_code'
```

### See All Metric Scores
```bash
curl ... | jq '.results[] | {model, overall_score, metrics}'
```

## ❌ Common Errors & Fixes

### Error: "Port 5000 already in use"
**Fix:** The app now uses port 5001 by default. Update your curl commands to use `http://localhost:5001`

### Error: "models/gemini-1.5-pro is not found"
**Fix:** Use Gemini 2.x models instead:
- Replace `gemini-1.5-pro` → `gemini-2.5-pro`
- Replace `gemini-1.5-flash` → `gemini-2.0-flash`

### Error: "GOOGLE_API_KEY must be set"
**Fix:**
```bash
export GOOGLE_API_KEY=your_actual_api_key
```

### Error: Connection refused
**Fix:** Make sure the server is running:
```bash
# Check if running
curl http://localhost:5001/health

# If not, start it
python app.py
```

## 🎯 Next Steps

1. ✅ Server is running on port 5001
2. ✅ Using correct Gemini 2.x model names
3. ✅ API is working correctly

Try the working examples:
```bash
./working_examples.sh
```

Or test specific prompts:
```bash
curl -X POST http://localhost:5001/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "YOUR CODING TASK HERE",
    "models": ["gemini-2.0-flash-exp", "gemini-2.0-flash"]
  }' | jq '.'
```

## 📚 Full Documentation

- [README.md](README.md) - Complete project documentation
- [CURL_EXAMPLES.md](CURL_EXAMPLES.md) - All curl command examples
- [SRS.md](SRS.md) - Software Requirements Specification

Happy coding! 🚀
