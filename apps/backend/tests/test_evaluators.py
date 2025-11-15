"""
Unit tests for metric analyzer modules
"""

import pytest
from anubis.evaluators import (
    ReadabilityAnalyzer,
    ConsistencyAnalyzer,
    ComplexityAnalyzer,
    DocumentationAnalyzer,
    DependencyAnalyzer
)


class TestReadabilityAnalyzer:
    """Test cases for ReadabilityAnalyzer."""

    def test_well_written_code(self):
        """Test analysis of well-written code."""
        analyzer = ReadabilityAnalyzer()
        code = '''
def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    # Check for empty list
    if not numbers:
        return 0
    # Calculate sum and divide by count
    return sum(numbers) / len(numbers)
'''
        result = analyzer.analyze(code)
        assert result['score'] > 7.0
        assert 'notes' in result

    def test_poorly_written_code(self):
        """Test analysis of poorly written code."""
        analyzer = ReadabilityAnalyzer()
        code = 'def f(x):\n a=1\n b=2\n return a+b'
        result = analyzer.analyze(code)
        assert result['score'] < 8.0

    def test_syntax_error_code(self):
        """Test analysis of code with syntax errors."""
        analyzer = ReadabilityAnalyzer()
        code = 'def broken(\n    pass'
        result = analyzer.analyze(code)
        assert result['score'] == 0
        assert 'syntax error' in result['notes'].lower()


class TestConsistencyAnalyzer:
    """Test cases for ConsistencyAnalyzer."""

    def test_consistent_snake_case(self):
        """Test analysis of consistent snake_case naming."""
        analyzer = ConsistencyAnalyzer()
        code = '''
def my_function():
    my_variable = 10
    another_variable = 20
    return my_variable + another_variable
'''
        result = analyzer.analyze(code)
        assert result['score'] > 8.0

    def test_mixed_naming_conventions(self):
        """Test analysis of mixed naming conventions."""
        analyzer = ConsistencyAnalyzer()
        code = '''
def myFunction():
    my_variable = 10
    anotherVariable = 20
    return my_variable + anotherVariable
'''
        result = analyzer.analyze(code)
        assert result['score'] < 8.0


class TestComplexityAnalyzer:
    """Test cases for ComplexityAnalyzer."""

    def test_constant_time_complexity(self):
        """Test detection of O(1) complexity."""
        analyzer = ComplexityAnalyzer()
        code = 'def get_first(arr):\n    return arr[0] if arr else None'
        result = analyzer.analyze(code)
        assert result['detected_complexity'] == 'O(1)'
        assert result['score'] == 10.0

    def test_linear_time_complexity(self):
        """Test detection of O(n) complexity."""
        analyzer = ComplexityAnalyzer()
        code = '''
def sum_array(arr):
    total = 0
    for num in arr:
        total += num
    return total
'''
        result = analyzer.analyze(code)
        assert result['detected_complexity'] == 'O(n)'
        assert result['score'] == 9.0

    def test_quadratic_time_complexity(self):
        """Test detection of O(n²) complexity."""
        analyzer = ComplexityAnalyzer()
        code = '''
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr)):
            if arr[i] < arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
'''
        result = analyzer.analyze(code)
        assert result['detected_complexity'] == 'O(n²)'
        assert result['score'] == 6.5


class TestDocumentationAnalyzer:
    """Test cases for DocumentationAnalyzer."""

    def test_well_documented_code(self):
        """Test analysis of well-documented code."""
        analyzer = DocumentationAnalyzer()
        code = '''
def calculate_factorial(n):
    """
    Calculate the factorial of a number.

    Args:
        n: A positive integer

    Returns:
        The factorial of n
    """
    if n <= 1:
        return 1
    return n * calculate_factorial(n - 1)
'''
        result = analyzer.analyze(code)
        assert result['score'] > 7.0

    def test_undocumented_code(self):
        """Test analysis of undocumented code."""
        analyzer = DocumentationAnalyzer()
        code = 'def calc(n):\n    return n * 2'
        result = analyzer.analyze(code)
        assert result['score'] < 7.0


class TestDependencyAnalyzer:
    """Test cases for DependencyAnalyzer."""

    def test_no_dependencies(self):
        """Test analysis of code with no dependencies."""
        analyzer = DependencyAnalyzer()
        code = 'def add(a, b):\n    return a + b'
        result = analyzer.analyze(code)
        assert result['score'] == 10.0
        assert result['dependencies_count'] == 0

    def test_standard_library_only(self):
        """Test analysis of code using only standard library."""
        analyzer = DependencyAnalyzer()
        code = '''
import os
import sys
from datetime import datetime

def get_current_time():
    return datetime.now()
'''
        result = analyzer.analyze(code)
        assert result['score'] == 10.0
        assert result['dependencies_count'] == 0

    def test_external_dependencies(self):
        """Test analysis of code with external dependencies."""
        analyzer = DependencyAnalyzer()
        code = '''
import requests
import pandas
from numpy import array

def fetch_data():
    return requests.get('http://example.com')
'''
        result = analyzer.analyze(code)
        assert result['dependencies_count'] == 3
        assert result['score'] < 10.0
