"""
Base Analyzer Class
"""

from abc import ABC, abstractmethod
from typing import Dict


class BaseAnalyzer(ABC):
    """Abstract base class for all metric analyzers."""

    @abstractmethod
    def analyze(self, code: str) -> Dict[str, any]:
        """
        Analyze code and return metric scores.

        Args:
            code: The code to analyze.

        Returns:
            Dictionary containing:
                - score: Numeric score (0-10)
                - notes: Text description of the analysis
                - Additional metric-specific fields
        """
        pass
