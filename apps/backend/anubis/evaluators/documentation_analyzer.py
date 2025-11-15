"""
Documentation Analyzer
Evaluates code documentation quality (docstrings and comments).
"""

import ast
from typing import Dict
from .base_analyzer import BaseAnalyzer


class DocumentationAnalyzer(BaseAnalyzer):
    """Analyzes code documentation."""

    def analyze(self, code: str) -> Dict[str, any]:
        """
        Analyze code documentation.

        Args:
            code: The code to analyze.

        Returns:
            Dictionary with documentation score and notes.
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {
                'score': 0,
                'notes': 'Code has syntax errors'
            }

        docstring_score = self._evaluate_docstrings(tree)
        comment_score = self._evaluate_inline_comments(code)

        overall_score = (docstring_score * 0.7 + comment_score * 0.3)

        notes = self._generate_notes(docstring_score, comment_score)

        return {
            'score': round(overall_score, 1),
            'notes': notes
        }

    def _evaluate_docstrings(self, tree: ast.AST) -> float:
        """Evaluate docstring presence and quality (0-10)."""
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

        if not functions and not classes:
            # No functions or classes to document
            return 7.0

        documented = 0
        total = len(functions) + len(classes)

        for node in functions + classes:
            docstring = ast.get_docstring(node)
            if docstring:
                # Award more points for detailed docstrings
                if len(docstring) > 50:
                    documented += 1.0
                elif len(docstring) > 20:
                    documented += 0.7
                else:
                    documented += 0.5

        if total == 0:
            return 7.0

        documentation_ratio = documented / total

        if documentation_ratio >= 0.9:
            return 10.0
        elif documentation_ratio >= 0.7:
            return 8.5
        elif documentation_ratio >= 0.5:
            return 7.0
        elif documentation_ratio >= 0.3:
            return 5.0
        else:
            return 3.0

    def _evaluate_inline_comments(self, code: str) -> float:
        """Evaluate inline comment quality (0-10)."""
        lines = code.split('\n')
        code_lines = [l for l in lines if l.strip() and not l.strip().startswith('#')]
        inline_comments = [l for l in lines if '#' in l and not l.strip().startswith('#')]

        if not code_lines:
            return 5.0

        # Look for inline comments within code lines
        comment_ratio = len(inline_comments) / len(code_lines)

        if 0.05 <= comment_ratio <= 0.2:
            return 10.0
        elif 0.02 <= comment_ratio < 0.05:
            return 7.0
        elif comment_ratio > 0.2:
            return 8.0
        else:
            return 5.0

    def _generate_notes(self, docstring_score: float, comment_score: float) -> str:
        """Generate human-readable notes about documentation."""
        notes = []

        if docstring_score >= 8:
            notes.append("Excellent docstrings")
        elif docstring_score >= 6:
            notes.append("Good docstrings")
        elif docstring_score >= 4:
            notes.append("Missing some docstrings")
        else:
            notes.append("Lacks proper docstrings")

        if comment_score >= 7:
            notes.append("appropriate inline comments")
        else:
            notes.append("could use more inline comments")

        return ", ".join(notes)
