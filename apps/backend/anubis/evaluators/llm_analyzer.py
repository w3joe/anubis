"""
LLM Analyzer Module
Uses Gemini 2.5 Pro to analyze generated code and provide pros and cons.
"""

import os
import json
from typing import Dict, Optional
from google import genai


class LLMAnalyzer:
    """Analyzes code using Gemini 2.5 Pro to provide pros and cons arrays."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the LLM Analyzer.

        Args:
            api_key: Google API key. If None, reads from GOOGLE_API_KEY env var.
        """
        self.api_key = api_key or os.environ.get('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY must be set in environment or passed as parameter")

        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.5-pro"  # Using Gemini 2.5 Pro for code analysis

    def analyze(self, code: str) -> Dict[str, any]:
        """
        Analyze code using Gemini 2.5 Pro and return pros, cons, and language.

        Args:
            code: The code to analyze.

        Returns:
            Dictionary containing:
                - pros: Array of positive aspects (point form)
                - cons: Array of negative aspects (point form)
                - language: Detected programming language
        """
        if not code or not code.strip():
            return {
                'pros': [],
                'cons': ['No code was generated'],
                'language': 'unknown'
            }

        # Detect language from code first
        detected_language = self._detect_language_from_code(code)

        try:
            # Create analysis prompt
            analysis_prompt = self._build_analysis_prompt(code, detected_language)

            # Call Gemini API
            response = self.client.models.generate_content(
                model=self.model,
                contents=analysis_prompt
            )

            # Parse response
            analysis_result = self._parse_response(response.text)
            
            # Override language with detected language if LLM returned unknown or wrong
            if detected_language != 'unknown':
                analysis_result['language'] = detected_language

            return analysis_result

        except Exception as e:
            # Return error result
            return {
                'pros': [],
                'cons': [f'Failed to analyze code: {str(e)}'],
                'language': detected_language if detected_language != 'unknown' else 'unknown'
            }

    def _detect_language_from_code(self, code: str) -> str:
        """
        Detect programming language from code content.

        Args:
            code: The code to analyze.

        Returns:
            Detected language string.
        """
        code_lower = code.lower().strip()
        
        # Check for Python - most common patterns first
        python_indicators = [
            'def ', 'import ', 'from ', 'print(', 'if __name__', 
            'class ', 'lambda ', 'yield ', 'elif ', 'except ', 
            'with ', 'as ', 'pass', 'return ', 'self.'
        ]
        python_count = sum(1 for indicator in python_indicators if indicator in code)
        
        # Python is likely if we see multiple Python keywords
        if python_count >= 2:
            return 'Python'
        # Or if we see very specific Python patterns
        if 'def ' in code or ('import ' in code) or 'if __name__' in code or 'self.' in code:
            return 'Python'
        
        # Check for JavaScript/TypeScript
        js_keywords = ['function ', 'const ', 'let ', 'var ', '=>', 'console.log', 'export ', 'require(']
        if any(keyword in code for keyword in js_keywords):
            if 'function ' in code or 'const ' in code or '=>' in code or 'console.log' in code:
                return 'JavaScript'
        
        # Check for Java
        if 'public class' in code_lower or 'public static void main' in code_lower or 'package ' in code:
            if 'public class' in code_lower or 'public static void main' in code_lower:
                return 'Java'
        
        # Check for C++
        if '#include' in code or 'std::' in code or 'using namespace' in code or 'int main()' in code_lower:
            return 'C++'
        
        # Check for C#
        if 'using System' in code or ('namespace ' in code and 'class ' in code):
            if 'using System' in code:
                return 'C#'
        
        # Check for Go
        if 'package main' in code_lower or 'func main()' in code_lower or 'import "' in code:
            return 'Go'
        
        # Check for Rust
        if 'fn main()' in code_lower or ('use ' in code and '::' in code):
            return 'Rust'
        
        # Check for Ruby
        if 'def ' in code and 'end' in code and ('puts ' in code or 'require ' in code):
            return 'Ruby'
        
        # Check for PHP
        if '<?php' in code or '<?=' in code:
            return 'PHP'
        
        # Check for TypeScript (more specific than JS)
        if 'interface ' in code or 'type ' in code or ': string' in code or ': number' in code:
            if 'interface ' in code or 'type ' in code:
                return 'TypeScript'
        
        return 'unknown'

    def _build_analysis_prompt(self, code: str, detected_language: str = 'unknown') -> str:
        """
        Build the prompt for code analysis.

        Args:
            code: The code to analyze.
            detected_language: Detected programming language.

        Returns:
            Formatted prompt string.
        """
        language_hint = f" (The code appears to be {detected_language})" if detected_language != 'unknown' else ""
        
        prompt = f"""Analyze the following code and provide a comprehensive analysis in JSON format.

Code:
```
{code}
```

Please provide your analysis in the following JSON structure:
{{
  "language": "detected programming language{language_hint}",
  "pros": [
    "list of positive aspects and strengths in point form",
    "each item should be a specific, actionable observation",
    "focus on code quality, best practices, and strengths"
  ],
  "cons": [
    "list of negative aspects and areas for improvement in point form",
    "each item should be a specific, actionable observation",
    "focus on issues, weaknesses, and areas needing improvement"
  ]
}}

Important:
- Be specific and actionable in your analysis
- Focus on code quality, best practices, and potential issues
- Identify both strengths and weaknesses
- The programming language appears to be {detected_language if detected_language != 'unknown' else 'unknown (detect it)'}
- Return ONLY valid JSON, no markdown formatting or additional text
- Ensure pros and cons are arrays of strings in point form
"""
        return prompt

    def _parse_response(self, response_text: str) -> Dict[str, any]:
        """
        Parse the JSON response from Gemini.

        Args:
            response_text: Raw response text from Gemini.

        Returns:
            Parsed analysis dictionary.
        """
        # Try to extract JSON from markdown code blocks if present
        json_text = response_text.strip()

        # Remove markdown code blocks if present
        if '```json' in json_text:
            start = json_text.find('```json') + len('```json')
            end = json_text.find('```', start)
            if end != -1:
                json_text = json_text[start:end].strip()
        elif '```' in json_text:
            start = json_text.find('```') + len('```')
            end = json_text.find('```', start)
            if end != -1:
                json_text = json_text[start:end].strip()

        # Try to find JSON object in the text (look for { ... })
        if '{' in json_text and '}' in json_text:
            start_brace = json_text.find('{')
            # Find matching closing brace
            brace_count = 0
            end_brace = -1
            for i in range(start_brace, len(json_text)):
                if json_text[i] == '{':
                    brace_count += 1
                elif json_text[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_brace = i + 1
                        break
            if end_brace > start_brace:
                json_text = json_text[start_brace:end_brace]

        try:
            # Parse JSON
            analysis = json.loads(json_text)

            # Validate and structure the response
            result = {
                'pros': analysis.get('pros', []),
                'cons': analysis.get('cons', []),
                'language': analysis.get('language', 'unknown')
            }

            # Ensure pros and cons are lists
            if not isinstance(result['pros'], list):
                result['pros'] = [str(result['pros'])] if result['pros'] else []
            if not isinstance(result['cons'], list):
                result['cons'] = [str(result['cons'])] if result['cons'] else []

            return result

        except json.JSONDecodeError as e:
            # If JSON parsing fails, try to extract information manually
            return {
                'pros': [],
                'cons': [f'Could not parse analysis response: {str(e)}'],
                'language': self._detect_language_fallback(response_text)
            }

    def _detect_language_fallback(self, text: str) -> str:
        """
        Fallback language detection from text analysis.

        Args:
            text: Response text to analyze.

        Returns:
            Detected language string.
        """
        text_lower = text.lower()
        if 'python' in text_lower:
            return 'Python'
        elif 'javascript' in text_lower or 'typescript' in text_lower:
            return 'JavaScript'
        elif 'java' in text_lower:
            return 'Java'
        elif 'c++' in text_lower or 'cpp' in text_lower:
            return 'C++'
        elif 'c#' in text_lower or 'csharp' in text_lower:
            return 'C#'
        elif 'go' in text_lower or 'golang' in text_lower:
            return 'Go'
        elif 'rust' in text_lower:
            return 'Rust'
        elif 'ruby' in text_lower:
            return 'Ruby'
        elif 'php' in text_lower:
            return 'PHP'
        else:
            return 'unknown'

