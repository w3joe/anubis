#!/bin/bash

# Test script for weighted metrics evaluation
# This script demonstrates the new metrics priority feature

echo "=========================================="
echo "Testing Anubis Weighted Metrics System"
echo "=========================================="
echo ""

# Test 1: Without metrics priority (uses default equal weights)
echo "Test 1: Default evaluation (no metrics priority)"
echo "------------------------------------------"
curl -s -X POST http://localhost:5001/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function to check if a number is prime",
    "models": ["gemini-2.0-flash-exp"]
  }' | jq '.'

echo ""
echo ""

# Test 2: Prioritize time complexity (performance-focused)
echo "Test 2: Prioritize TIME COMPLEXITY (performance first)"
echo "------------------------------------------"
curl -s -X POST http://localhost:5001/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function to check if a number is prime",
    "models": ["gemini-2.0-flash-exp"],
    "metrics": ["time_complexity", "readability", "consistency", "code_documentation", "external_dependencies"]
  }' | jq '.'

echo ""
echo ""

# Test 3: Prioritize documentation (code clarity focused)
echo "Test 3: Prioritize DOCUMENTATION (clarity first)"
echo "------------------------------------------"
curl -s -X POST http://localhost:5001/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function to check if a number is prime",
    "models": ["gemini-2.0-flash-exp"],
    "metrics": ["code_documentation", "readability", "consistency", "time_complexity", "external_dependencies"]
  }' | jq '.'

echo ""
echo ""

# Test 4: Compare multiple models with weighted metrics
echo "Test 4: Compare 2 models with READABILITY priority"
echo "------------------------------------------"
curl -s -X POST http://localhost:5001/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function to find the longest common subsequence",
    "models": ["gemini-2.0-flash-exp", "gemini-1.5-flash"],
    "metrics": ["readability", "code_documentation", "consistency", "time_complexity", "external_dependencies"]
  }' | jq '.summary'

echo ""
echo ""
echo "=========================================="
echo "Testing complete!"
echo "=========================================="
