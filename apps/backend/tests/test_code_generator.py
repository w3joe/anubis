"""
Unit tests for CodeGenerator module
"""

import pytest
from unittest.mock import Mock, patch
from anubis.code_generator import CodeGenerator


class TestCodeGenerator:
    """Test cases for CodeGenerator class."""

    def test_init_with_api_key(self):
        """Test initialization with API key."""
        generator = CodeGenerator(api_key="test_key")
        assert generator.api_key == "test_key"
        assert generator.max_retries == 3

    def test_init_without_api_key_raises_error(self):
        """Test initialization without API key raises ValueError."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="GOOGLE_API_KEY must be set"):
                CodeGenerator()

    def test_extract_code_with_python_markdown(self):
        """Test code extraction from markdown Python blocks."""
        generator = CodeGenerator(api_key="test_key")
        response = "```python\ndef hello():\n    print('world')\n```"
        extracted = generator._extract_code(response)
        assert extracted == "def hello():\n    print('world')"

    def test_extract_code_with_generic_markdown(self):
        """Test code extraction from generic markdown blocks."""
        generator = CodeGenerator(api_key="test_key")
        response = "```\ndef hello():\n    print('world')\n```"
        extracted = generator._extract_code(response)
        assert extracted == "def hello():\n    print('world')"

    def test_extract_code_without_markdown(self):
        """Test code extraction without markdown formatting."""
        generator = CodeGenerator(api_key="test_key")
        response = "def hello():\n    print('world')"
        extracted = generator._extract_code(response)
        assert extracted == "def hello():\n    print('world')"

    @patch('anubis.code_generator.genai.Client')
    def test_generate_code_success(self, mock_client):
        """Test successful code generation."""
        # Setup mock
        mock_response = Mock()
        mock_response.text = "```python\ndef test():\n    pass\n```"
        mock_client.return_value.models.generate_content.return_value = mock_response

        generator = CodeGenerator(api_key="test_key")
        result = generator.generate_code("Write a test function", "gemini-2.0-flash-exp")

        assert result['success'] is True
        assert 'def test():' in result['generated_code']
        assert result['model'] == "gemini-2.0-flash-exp"
        assert result['execution_time_ms'] > 0

    @patch('anubis.code_generator.genai.Client')
    def test_generate_code_failure_with_retry(self, mock_client):
        """Test code generation failure after retries."""
        # Setup mock to always fail
        mock_client.return_value.models.generate_content.side_effect = Exception("API Error")

        generator = CodeGenerator(api_key="test_key", max_retries=2)
        result = generator.generate_code("Write a test function", "gemini-2.0-flash-exp")

        assert result['success'] is False
        assert result['error'] == "API Error"
        assert result['generated_code'] == ''
        # Should have tried 2 times
        assert mock_client.return_value.models.generate_content.call_count == 2
