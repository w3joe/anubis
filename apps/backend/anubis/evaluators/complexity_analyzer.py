"""
Complexity Analyzer
Analyzes time and space complexity of code.
"""

import ast
import re
from typing import Dict
from .base_analyzer import BaseAnalyzer


class ComplexityAnalyzer(BaseAnalyzer):
    """Analyzes code complexity."""

    def analyze(self, code: str) -> Dict[str, any]:
        """
        Analyze code complexity.

        Args:
            code: The code to analyze.

        Returns:
            Dictionary with complexity score, detected complexity, and notes.
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {
                'score': 0,
                'detected_complexity': 'Unknown',
                'notes': 'Code has syntax errors'
            }

        complexity = self._detect_complexity(tree, code)
        score = self._score_complexity(complexity)
        notes = self._generate_notes(complexity)

        return {
            'score': score,
            'detected_complexity': complexity,
            'notes': notes
        }

    def _detect_complexity(self, tree: ast.AST, code: str) -> str:
        """Detect the time complexity of the code."""
        # Check for nested loops
        max_loop_depth = self._get_max_loop_depth(tree)

        # Check for recursive functions
        has_recursion = self._has_recursion(tree)

        # Check for common patterns
        has_sorting = 'sort' in code.lower()
        has_binary_search = 'binary' in code.lower() and 'search' in code.lower()

        # Determine complexity based on patterns
        if has_recursion:
            # Could be exponential or logarithmic
            if 'fibonacci' in code.lower():
                return 'O(2^n)'
            elif has_binary_search or 'divide' in code.lower():
                return 'O(log n)'
            else:
                return 'O(n)'

        if max_loop_depth >= 3:
            return 'O(n³)'
        elif max_loop_depth == 2:
            return 'O(n²)'
        elif max_loop_depth == 1:
            if has_sorting:
                return 'O(n log n)'
            else:
                return 'O(n)'
        else:
            return 'O(1)'

    def _get_max_loop_depth(self, tree: ast.AST, current_depth: int = 0) -> int:
        """Calculate maximum loop nesting depth."""
        max_depth = current_depth

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.For, ast.While)):
                depth = self._get_max_loop_depth(node, current_depth + 1)
                max_depth = max(max_depth, depth)
            else:
                depth = self._get_max_loop_depth(node, current_depth)
                max_depth = max(max_depth, depth)

        return max_depth

    def _has_recursion(self, tree: ast.AST) -> bool:
        """Check if code contains recursive function calls."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Name) and child.func.id == func_name:
                            return True
        return False

    def _score_complexity(self, complexity: str) -> float:
        """Score complexity based on efficiency (0-10)."""
        complexity_scores = {
            'O(1)': 10.0,
            'O(log n)': 9.5,
            'O(n)': 9.0,
            'O(n log n)': 8.0,
            'O(n²)': 6.5,
            'O(n³)': 4.0,
            'O(2^n)': 2.0,
            'Unknown': 5.0
        }

        return complexity_scores.get(complexity, 5.0)
    def _generate_notes(self, complexity: str) -> str:
        """Generate human-readable notes about complexity."""
        if complexity == 'O(1)':
            return 'Constant time - excellent efficiency'
        elif complexity == 'O(log n)':
            return 'Logarithmic time - very efficient'
        elif complexity == 'O(n)':
            return 'Linear time - good efficiency'
        elif complexity == 'O(n log n)':
            return 'Linearithmic time - efficient for sorting'
        elif complexity == 'O(n²)':
            return 'Quadratic time - acceptable for small inputs'
        elif complexity == 'O(n³)':
            return 'Cubic time - inefficient for large inputs'
        elif complexity == 'O(2^n)':
            return 'Exponential time - very inefficient'
        else:
            return 'Could not determine complexity'

