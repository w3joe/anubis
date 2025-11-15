"""
Consistency Analyzer
Evaluates naming convention consistency and code style uniformity.
"""

import ast
import re
from typing import Dict, List
from .base_analyzer import BaseAnalyzer


class ConsistencyAnalyzer(BaseAnalyzer):
    """Analyzes code consistency."""

    def analyze(self, code: str) -> Dict[str, any]:
        """
        Analyze code consistency.

        Args:
            code: The code to analyze.

        Returns:
            Dictionary with consistency score and notes.
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {
                'score': 0,
                'notes': 'Code has syntax errors'
            }

        naming_score = self._evaluate_naming_consistency(tree)
        style_score = self._evaluate_style_consistency(code)

        overall_score = (naming_score * 0.6 + style_score * 0.4)

        notes = self._generate_notes(naming_score, style_score)

        return {
            'score': round(overall_score, 1),
            'notes': notes
        }

    def _evaluate_naming_consistency(self, tree: ast.AST) -> float:
        """Evaluate naming convention consistency (0-10)."""
        snake_case_count = 0
        camel_case_count = 0
        other_count = 0

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.Name)):
                name = node.name if isinstance(node, ast.FunctionDef) else node.id

                if re.match(r'^[a-z_][a-z0-9_]*$', name):
                    snake_case_count += 1
                elif re.match(r'^[a-z][a-zA-Z0-9]*$', name):
                    camel_case_count += 1
                else:
                    other_count += 1

        total = snake_case_count + camel_case_count + other_count
        if total == 0:
            return 5.0

        # Calculate consistency (higher when one style dominates)
        max_style = max(snake_case_count, camel_case_count)
        consistency_ratio = max_style / total

        if consistency_ratio >= 0.9:
            return 10.0
        elif consistency_ratio >= 0.8:
            return 8.0
        elif consistency_ratio >= 0.7:
            return 6.0
        else:
            return 4.0

    def _evaluate_style_consistency(self, code: str) -> float:
        """Evaluate code style uniformity (0-10)."""
        score = 10.0

        lines = code.split('\n')

        # Check for mixed indentation
        has_tabs = any('\t' in line for line in lines)
        has_spaces = any(re.match(r'^ +', line) for line in lines)

        if has_tabs and has_spaces:
            score -= 3.0

        # Check for consistent quote usage
        single_quotes = code.count("'")
        double_quotes = code.count('"')
        total_quotes = single_quotes + double_quotes

        if total_quotes > 0:
            dominant_quote_ratio = max(single_quotes, double_quotes) / total_quotes
            if dominant_quote_ratio < 0.8:
                score -= 1.0

        return max(0, score)
    def _generate_notes(self, naming_score: float, style_score: float) -> str:
        """Generate human-readable notes about consistency."""
        notes = []

        if naming_score >= 8:
            notes.append("Consistent naming conventions")
        elif naming_score >= 6:
            notes.append("Mostly consistent naming")
        else:
            notes.append("Inconsistent naming conventions")

        if style_score >= 8:
            notes.append("uniform code style")
        else:
            notes.append("style inconsistencies found")

        return ", ".join(notes)

