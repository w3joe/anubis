"""
Readability Analyzer
Evaluates code readability based on variable naming, structure, and comments.
"""

import re
import ast
from typing import Dict
from .base_analyzer import BaseAnalyzer


class ReadabilityAnalyzer(BaseAnalyzer):
    """Analyzes code readability."""

    def analyze(self, code: str) -> Dict[str, any]:
        """
        Analyze code readability.

        Args:
            code: The code to analyze.

        Returns:
            Dictionary with readability score and notes.
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {
                'score': 0,
                'notes': 'Code has syntax errors'
            }

        # Initialize scoring components
        variable_naming_score = self._evaluate_variable_naming(code, tree)
        structure_score = self._evaluate_structure(tree)
        comment_score = self._evaluate_comments(code)

        # Calculate overall readability score
        overall_score = (
            variable_naming_score * 0.4 +
            structure_score * 0.4 +
            comment_score * 0.2
        )

        notes = self._generate_notes(
            variable_naming_score,
            structure_score,
            comment_score
        )

        return {
            'score': round(overall_score, 1),
            'notes': notes
        }

    def _evaluate_variable_naming(self, code: str, tree: ast.AST) -> float:
        """Evaluate variable naming quality (0-10)."""
        score = 10.0
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                name = node.id
                # Check for single-letter variables (except common ones like i, j, x, y)
                if len(name) == 1 and name not in ['i', 'j', 'k', 'x', 'y', 'n']:
                    score -= 0.5
                    issues.append(f"Single-letter variable: {name}")

                # Check for non-descriptive names
                if name in ['temp', 'tmp', 'var', 'data', 'foo', 'bar']:
                    score -= 0.3
                    issues.append(f"Non-descriptive variable: {name}")

        return max(0, score)

    def _evaluate_structure(self, tree: ast.AST) -> float:
        """Evaluate code structure and organization (0-10)."""
        score = 10.0

        # Check for excessively long functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_length = len(node.body)
                if func_length > 50:
                    score -= 2.0
                elif func_length > 30:
                    score -= 1.0

        # Check for nested depth
        max_depth = self._get_max_nesting_depth(tree)
        if max_depth > 4:
            score -= 2.0
        elif max_depth > 3:
            score -= 1.0

        return max(0, score)

    def _evaluate_comments(self, code: str) -> float:
        """Evaluate presence and quality of comments (0-10)."""
        lines = code.split('\n')
        code_lines = [l for l in lines if l.strip() and not l.strip().startswith('#')]
        comment_lines = [l for l in lines if l.strip().startswith('#')]

        if not code_lines:
            return 5.0

        comment_ratio = len(comment_lines) / len(code_lines)

        # Ideal ratio is around 0.1-0.3 (10-30% comments)
        if 0.1 <= comment_ratio <= 0.3:
            return 10.0
        elif 0.05 <= comment_ratio < 0.1:
            return 7.0
        elif comment_ratio > 0.3:
            return 8.0  # Too many comments can clutter
        else:
            return 5.0  # Too few comments

    def _get_max_nesting_depth(self, tree: ast.AST, current_depth: int = 0) -> int:
        """Calculate maximum nesting depth in the code."""
        max_depth = current_depth

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                depth = self._get_max_nesting_depth(node, current_depth + 1)
                max_depth = max(max_depth, depth)

        return max_depth

    def _generate_notes(
        self,
        variable_score: float,
        structure_score: float,
        comment_score: float
    ) -> str:
        """Generate human-readable notes about readability."""
        notes = []

        if variable_score >= 8:
            notes.append("Clear variable names")
        elif variable_score >= 6:
            notes.append("Variable names could be more descriptive")
        else:
            notes.append("Poor variable naming")

        if structure_score >= 8:
            notes.append("well-structured")
        elif structure_score >= 6:
            notes.append("structure needs improvement")
        else:
            notes.append("poorly structured")

        if comment_score >= 8:
            notes.append("appropriate comments")
        elif comment_score >= 6:
            notes.append("could use more comments")
        else:
            notes.append("lacks sufficient comments")

        return ", ".join(notes)
