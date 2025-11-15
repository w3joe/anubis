"""
IssuesAnalyzer Module
Analyzes code for potential issues, bugs, and improvements.
"""

import ast
import re
from typing import Dict, List
from .base_analyzer import BaseAnalyzer


class IssuesAnalyzer(BaseAnalyzer):
    """Analyzes code for potential issues and improvement areas."""

    def analyze(self, code: str) -> Dict[str, any]:
        """
        Analyze code for potential issues.

        Args:
            code: The code to analyze.

        Returns:
            Dictionary containing potential issues as a list of strings.
        """
        issues = []

        try:
            # Parse the code into AST
            tree = ast.parse(code)

            # Check for various potential issues
            issues.extend(self._check_error_handling(tree, code))
            issues.extend(self._check_edge_cases(tree, code))
            issues.extend(self._check_security_issues(code))
            issues.extend(self._check_performance_concerns(tree, code))
            issues.extend(self._check_best_practices(tree, code))

        except SyntaxError:
            issues.append("Code contains syntax errors")
        except Exception as e:
            issues.append(f"Unable to fully analyze code: {str(e)}")

        # Format issues as a single paragraph with bullet points
        if not issues:
            issues_text = "No significant issues detected."
        else:
            issues_text = " • ".join(issues)

        return {
            'issues': issues,
            'issues_text': issues_text,
            'issues_count': len(issues)
        }

    def _check_error_handling(self, tree: ast.AST, code: str) -> List[str]:
        """Check for missing or inadequate error handling."""
        issues = []

        # Check if there are any try-except blocks
        has_try_except = any(isinstance(node, ast.Try) for node in ast.walk(tree))

        # Check for operations that might fail without error handling
        risky_operations = []
        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
                risky_operations.append("division")
            elif isinstance(node, ast.Subscript):
                risky_operations.append("indexing")

        if risky_operations and not has_try_except:
            issues.append(f"Missing error handling for {', '.join(set(risky_operations))} operations")

        return issues

    def _check_edge_cases(self, tree: ast.AST, code: str) -> List[str]:
        """Check for potential edge case handling issues."""
        issues = []

        # Look for functions that might not handle None or empty inputs
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check if function validates input parameters
                has_input_validation = any(
                    isinstance(n, ast.If) for n in ast.walk(node)
                )

                # Check if function has parameters
                if node.args.args and not has_input_validation:
                    issues.append(f"Function '{node.name}' may not validate input parameters (None, empty values)")

        return issues

    def _check_security_issues(self, code: str) -> List[str]:
        """Check for potential security issues."""
        issues = []

        # Check for dangerous functions
        dangerous_patterns = [
            (r'\beval\s*\(', "Use of eval() is a security risk"),
            (r'\bexec\s*\(', "Use of exec() is a security risk"),
            (r'__import__\s*\(', "Dynamic imports may pose security risks"),
        ]

        for pattern, message in dangerous_patterns:
            if re.search(pattern, code):
                issues.append(message)

        return issues

    def _check_performance_concerns(self, tree: ast.AST, code: str) -> List[str]:
        """Check for potential performance issues."""
        issues = []

        # Check for nested loops (potential O(n²) or worse)
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                # Check if there's another loop inside
                for child in ast.walk(node):
                    if child != node and isinstance(child, (ast.For, ast.While)):
                        issues.append("Nested loops detected - consider algorithm optimization for large inputs")
                        break

        # Check for list comprehensions inside loops
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                for child in ast.walk(node):
                    if isinstance(child, ast.ListComp):
                        issues.append("List comprehension inside loop may impact performance")
                        break

        return issues

    def _check_best_practices(self, tree: ast.AST, code: str) -> List[str]:
        """Check for violations of Python best practices."""
        issues = []

        # Check for bare except clauses
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    issues.append("Bare except clause found - should catch specific exceptions")

        # Check for mutable default arguments
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for default in node.args.defaults:
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        issues.append(f"Function '{node.name}' uses mutable default argument - may cause unexpected behavior")

        # Check for print statements in functions (should use logging or return values)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Name) and child.func.id == 'print':
                            issues.append(f"Function '{node.name}' contains print statements - consider using return values or logging")
                            break

        return issues
