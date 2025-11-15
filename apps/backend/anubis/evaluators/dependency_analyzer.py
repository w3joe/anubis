"""
Dependency Analyzer
Evaluates external dependencies and standard library usage.
"""

import ast
from typing import Dict, List, Set
from .base_analyzer import BaseAnalyzer


class DependencyAnalyzer(BaseAnalyzer):
    """Analyzes code dependencies."""

    # Python standard library modules (partial list of common ones)
    STANDARD_LIBRARY = {
        'os', 'sys', 'math', 'random', 'datetime', 'time', 'json', 'csv',
        're', 'collections', 'itertools', 'functools', 'typing', 'pathlib',
        'unittest', 'logging', 'argparse', 'subprocess', 'threading', 'multiprocessing',
        'io', 'shutil', 'tempfile', 'glob', 'pickle', 'copy', 'string', 'textwrap',
        'abc', 'contextlib', 'warnings', 'weakref', 'ast', 'dis', 'inspect'
    }

    def analyze(self, code: str) -> Dict[str, any]:
        """
        Analyze code dependencies.

        Args:
            code: The code to analyze.

        Returns:
            Dictionary with dependency score, count, and notes.
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {
                'score': 0,
                'dependencies_count': 0,
                'notes': 'Code has syntax errors'
            }

        dependencies = self._extract_dependencies(tree)
        external_deps = self._count_external_dependencies(dependencies)
        score = self._score_dependencies(external_deps, dependencies)
        notes = self._generate_notes(external_deps, dependencies)

        return {
            'score': score,
            'dependencies_count': external_deps,
            'notes': notes
        }

    def _extract_dependencies(self, tree: ast.AST) -> Set[str]:
        """Extract all imported modules."""
        dependencies = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # Get the base module name
                    module = alias.name.split('.')[0]
                    dependencies.add(module)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    # Get the base module name
                    module = node.module.split('.')[0]
                    dependencies.add(module)

        return dependencies

    def _count_external_dependencies(self, dependencies: Set[str]) -> int:
        """Count non-standard library dependencies."""
        external = 0
        for dep in dependencies:
            if dep not in self.STANDARD_LIBRARY:
                external += 1
        return external

    def _score_dependencies(self, external_count: int, all_deps: Set[str]) -> float:
        """Score based on dependency count (0-10)."""
        # Fewer external dependencies is better
        if external_count == 0:
            return 10.0
        elif external_count == 1:
            return 9.0
        elif external_count == 2:
            return 8.0
        elif external_count == 3:
            return 7.0
        elif external_count <= 5:
            return 6.0
        else:
            return max(3.0, 10.0 - external_count)
    def _generate_notes(self, external_count: int, all_deps: Set[str]) -> str:
        """Generate human-readable notes about dependencies."""
        if external_count == 0:
            if len(all_deps) == 0:
                return 'No external dependencies'
            else:
                return 'Uses only standard library'
        elif external_count == 1:
            return 'Minimal external dependencies'
        elif external_count <= 3:
            return 'Few external dependencies'
        else:
            return f'Many external dependencies ({external_count})'

