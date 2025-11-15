# ✅ Anubis Backend - All Issues Fixed!

## Changes Made

### 1. Flask Server Configuration
- ✅ **Host**: Now uses `localhost` (instead of `0.0.0.0`)
- ✅ **Port**: Now uses `5000` (standard Flask port)
- ✅ Location: [app.py:193-194](app.py#L193-L194)

### 2. NPM Scripts Fixed
- ✅ **dev script**: Now properly loads `.env` file with `set -a && source .env && set +a`
- ✅ **start script**: Same fix applied
- ✅ This correctly exports `GOOGLE_API_KEY` environment variable
- ✅ Location: [package.json:7-8](package.json#L7-L8)

### 3. Model Names Updated
- ✅ Removed deprecated models (`gemini-1.5-pro`, `gemini-1.5-flash`)
- ✅ Added current models:
  - `gemini-2.0-flash-exp` (recommended)
  - `gemini-2.0-flash`
  - `gemini-2.5-flash`
  - `gemini-2.5-pro`
  - `gemini-flash-latest`
  - `gemini-pro-latest`
- ✅ Location: [config.yaml:11-16](config.yaml#L11-L16)

### 4. Documentation Updated
- ✅ All port references changed to `5000`
- ✅ All model names updated to Gemini 2.x series

## 🚀 How to Start the Server

### Method 1: Using NPM/PNPM (Recommended)
```bash
cd /Users/w3joe/Documents/projects/anubis/apps/backend
npm run dev
# or
pnpm dev
```

### Method 2: Using Python Directly
```bash
cd /Users/w3joe/Documents/projects/anubis/apps/backend
source .venv/bin/activate
set -a && source .env && set +a
python app.py
```

### Method 3: One-Liner
```bash
cd /Users/w3joe/Documents/projects/anubis/apps/backend && source .venv/bin/activate && set -a && source .env && set +a && python app.py
```

## ✅ Verify Server is Running

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy"
}
```

## 📝 Test the API

### Single Model Test
```bash
curl -X POST http://localhost:5000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function to check if a number is prime",
    "models": ["gemini-2.0-flash-exp"]
  }' | jq '.'
```

### Multiple Models Comparison
```bash
curl -X POST http://localhost:5000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a binary search function with proper documentation",
    "models": ["gemini-2.0-flash-exp", "gemini-2.0-flash", "gemini-2.5-flash"]
  }' | jq '.ranking'
```

## ✅ What Was Fixed

### Problem 1: npm script errors with .env comments
**Before:**
```json
"dev": "export $(cat .env | xargs) && python app.py"
```
**Error:** `export: '#': not a valid identifier`

**After:**
```json
"dev": "set -a && source .env && set +a && python app.py"
```
**Result:** ✅ Properly loads all environment variables including GOOGLE_API_KEY

### Problem 2: Missing GOOGLE_API_KEY
**Before:** Environment variable not loaded when using npm scripts

**After:** ✅ API key properly loaded from `.env` file

### Problem 3: Port conflict with macOS AirPlay
**Before:** Used port `5001` to avoid conflict

**After:** ✅ Using standard port `5000` with `localhost` binding (no conflict)

### Problem 4: Deprecated model names
**Before:** Used `gemini-1.5-pro`, `gemini-1.5-flash`

**Error:** `models/gemini-1.5-pro is not found`

**After:** ✅ Using Gemini 2.x models

## 🎯 Current Status

- ✅ Server configuration: `localhost:5000`
- ✅ Environment variables: Loading correctly from `.env`
- ✅ API key: Set and working
- ✅ Models: All using Gemini 2.x series
- ✅ Documentation: Updated with correct ports and models

## 📚 Available Models

Use any of these in your API requests:
```json
{
  "models": [
    "gemini-2.0-flash-exp",    // Fastest, recommended
    "gemini-2.0-flash",         // Stable
    "gemini-2.5-flash",         // Newer, faster
    "gemini-2.5-pro",           // More capable
    "gemini-flash-latest",      // Latest flash version
    "gemini-pro-latest"         // Latest pro version
  ]
}
```

## 🎉 Everything is Working!

Start your server with:
```bash
npm run dev
```

Then test it with:
```bash
curl http://localhost:5000/health
```

Happy coding! 🚀
