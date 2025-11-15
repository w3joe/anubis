"""
CodeEvaluator Module
Orchestrates metric evaluation and score calculation.
"""

from typing import Dict, List
import yaml
from .evaluators import (
    ReadabilityAnalyzer,
    ConsistencyAnalyzer,
    ComplexityAnalyzer,
    DocumentationAnalyzer,
    DependencyAnalyzer
)


class CodeEvaluator:
    """Evaluates generated code using multiple metric analyzers."""

    DEFAULT_WEIGHTS = {
        'readability': 0.2,
        'consistency': 0.2,
        'time_complexity': 0.2,
        'code_documentation': 0.2,
        'external_dependencies': 0.2
    }

    def __init__(self, config_path: str = None):
        """
        Initialize the CodeEvaluator.

        Args:
            config_path: Path to config.yaml file. If None, uses default weights.
        """
        self.weights = self._load_weights(config_path)

        # Initialize analyzers
        self.analyzers = {
            'readability': ReadabilityAnalyzer(),
            'consistency': ConsistencyAnalyzer(),
            'time_complexity': ComplexityAnalyzer(),
            'code_documentation': DocumentationAnalyzer(),
            'external_dependencies': DependencyAnalyzer()
        }

    def _load_weights(self, config_path: str) -> Dict[str, float]:
        """Load metric weights from config file or use defaults."""
        if not config_path:
            return self.DEFAULT_WEIGHTS

        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config.get('metrics', {}).get('weights', self.DEFAULT_WEIGHTS)
        except Exception:
            return self.DEFAULT_WEIGHTS

    def evaluate(self, code: str, metrics_priority: List[str] = None) -> Dict[str, any]:
        """
        Evaluate code using all metric analyzers.

        Args:
            code: The code to evaluate.
            metrics_priority: Optional list of metrics in priority order.
                            Higher-ranked metrics get higher weights.

        Returns:
            Dictionary containing:
                - metrics: Individual metric scores and details
                - overall_score: Weighted average score
        """
        metrics = {}

        # Run each analyzer
        for metric_name, analyzer in self.analyzers.items():
            metrics[metric_name] = analyzer.analyze(code)

        # Calculate overall score with dynamic weights
        overall_score = self._calculate_overall_score(metrics, metrics_priority)

        return {
            'metrics': metrics,
            'overall_score': round(overall_score, 2)
        }

    def evaluate_multiple(self, code_samples: List[Dict[str, str]]) -> List[Dict[str, any]]:
        """
        Evaluate multiple code samples.

        Args:
            code_samples: List of dicts with 'model' and 'code' keys.

        Returns:
            List of evaluation results.
        """
        results = []
        for sample in code_samples:
            evaluation = self.evaluate(sample['code'])
            evaluation['model'] = sample['model']
            results.append(evaluation)

        return results

    def _calculate_overall_score(self, metrics: Dict[str, Dict], metrics_priority: List[str] = None) -> float:
        """
        Calculate weighted average of all metric scores.

        Args:
            metrics: Dictionary of metric results
            metrics_priority: Optional list of metrics in priority order.
                            Uses exponential decay for weights based on position.

        Returns:
            Weighted average score
        """
        if not metrics_priority:
            # Use default weights from config
            total_score = 0.0
            for metric_name, weight in self.weights.items():
                if metric_name in metrics:
                    metric_score = metrics[metric_name].get('score', 0)
                    total_score += metric_score * weight
            return total_score

        # Calculate dynamic weights based on priority order
        # Using exponential decay: weight = base_weight * decay_factor^position
        # This ensures higher-ranked metrics have significantly more impact
        weights = self._calculate_dynamic_weights(metrics_priority)

        total_score = 0.0
        for metric_name, weight in weights.items():
            if metric_name in metrics:
                metric_score = metrics[metric_name].get('score', 0)
                total_score += metric_score * weight

        return total_score

    def _calculate_dynamic_weights(self, metrics_priority: List[str]) -> Dict[str, float]:
        """
        Calculate weights based on metrics priority order.

        Uses exponential decay: higher-ranked metrics get exponentially higher weights.
        Formula: weight[i] = base * (decay_rate ^ i)
        Normalized so all weights sum to 1.0

        Args:
            metrics_priority: List of metrics in descending priority order

        Returns:
            Dictionary mapping metric names to normalized weights
        """
        if not metrics_priority:
            return self.DEFAULT_WEIGHTS

        # Exponential decay parameters
        # decay_rate of 0.7 means each subsequent metric gets 70% of previous weight
        decay_rate = 0.7

        # Calculate raw weights using exponential decay
        raw_weights = {}
        for position, metric_name in enumerate(metrics_priority):
            raw_weights[metric_name] = decay_rate ** position

        # Normalize weights to sum to 1.0
        total_weight = sum(raw_weights.values())
        normalized_weights = {
            metric: weight / total_weight
            for metric, weight in raw_weights.items()
        }

        return normalized_weights
