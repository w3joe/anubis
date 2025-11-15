#!/bin/bash

# Test script for streaming API endpoint
# This demonstrates real-time code generation with Server-Sent Events

echo "=========================================="
echo "Testing Anubis Streaming API"
echo "=========================================="
echo ""

echo "Streaming code generation from gemini-2.0-flash-exp..."
echo "Watch as code appears in real-time!"
echo ""
echo "------------------------------------------"

curl -N -X POST http://localhost:5001/api/v1/evaluate/stream \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function to check if a number is prime",
    "models": ["gemini-2.0-flash-exp"],
    "metrics": ["time_complexity", "readability", "consistency", "code_documentation", "external_dependencies"]
  }'

echo ""
echo ""
echo "=========================================="
echo "Streaming test complete!"
echo "=========================================="
