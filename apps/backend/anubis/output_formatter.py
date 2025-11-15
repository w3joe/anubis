"""
OutputFormatter Module
Structures evaluation results and generates rankings.
"""

from typing import Dict, List
from datetime import datetime
import uuid
from .evaluators.issues_analyzer import IssuesAnalyzer


class OutputFormatter:
    """Formats evaluation results into standardized JSON output."""

    @staticmethod
    def format_results(
        prompt: str,
        evaluations: List[Dict[str, any]],
        generation_results: List[Dict[str, any]]
    ) -> Dict[str, any]:
        """
        Format evaluation results into final output structure.

        Args:
            prompt: The original coding prompt.
            evaluations: List of evaluation results from CodeEvaluator.
            generation_results: List of generation results from CodeGenerator.

        Returns:
            Formatted output dictionary matching SRS schema.
        """
        # Merge generation and evaluation results
        results = []
        for gen_result in generation_results:
            model = gen_result['model']

            # Find matching evaluation
            eval_result = next(
                (e for e in evaluations if e.get('model') == model),
                None
            )

            if not eval_result:
                continue

            # Format metrics according to SRS schema
            formatted_metrics = OutputFormatter._format_metrics(eval_result['metrics'])

            result = {
                'model': model,
                'overall_score': eval_result.get('overall_score', 0),
                'generated_code': gen_result.get('generated_code', ''),
                'metrics': formatted_metrics,
                'execution_time_ms': gen_result.get('execution_time_ms', 0),
                'success': gen_result.get('success', True),
                'error': gen_result.get('error')
            }

            results.append(result)

        # Create ranking
        ranking = OutputFormatter._create_ranking(results)

        # Create summary
        summary = OutputFormatter._create_summary(results)

        # Build final output
        output = {
            'evaluation_id': f"eval_{uuid.uuid4().hex[:8]}",
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'prompt': prompt,
            'results': results,
            'ranking': ranking,
            'summary': summary
        }

        return output

    @staticmethod
    def _format_metrics(metrics: Dict[str, Dict]) -> Dict[str, Dict]:
        """Format metrics to match SRS schema."""
        formatted = {}

        for metric_name, metric_data in metrics.items():
            formatted[metric_name] = {
                'score': metric_data.get('score', 0),
                'notes': metric_data.get('notes', '')
            }

            # Add metric-specific fields
            if metric_name == 'time_complexity' and 'detected_complexity' in metric_data:
                formatted[metric_name]['detected_complexity'] = metric_data['detected_complexity']

            if metric_name == 'external_dependencies' and 'dependencies_count' in metric_data:
                formatted[metric_name]['dependencies_count'] = metric_data['dependencies_count']

        return formatted

    @staticmethod
    def _create_ranking(results: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """Create ranked list of models by overall score."""
        # Filter successful results only
        successful_results = [r for r in results if r.get('success', True)]

        # Sort by overall score (descending)
        sorted_results = sorted(
            successful_results,
            key=lambda x: x.get('overall_score', 0),
            reverse=True
        )

        # Create ranking
        ranking = []
        for rank, result in enumerate(sorted_results, start=1):
            ranking.append({
                'rank': rank,
                'model': result['model'],
                'score': result['overall_score']
            })

        return ranking

    @staticmethod
    def _create_summary(results: List[Dict[str, any]]) -> Dict[str, any]:
        """Create summary statistics including best generated code and potential issues."""
        successful_results = [r for r in results if r.get('success', True)]

        if not successful_results:
            return {
                'total_models_tested': len(results),
                'best_model': None,
                'best_score': 0,
                'best_generated_code': None,
                'potential_issues': None,
                'failed_evaluations': len(results),
                'successful_evaluations': 0
            }

        best_result = max(successful_results, key=lambda x: x.get('overall_score', 0))

        # Analyze best code for potential issues
        issues_analyzer = IssuesAnalyzer()
        best_code = best_result.get('generated_code', '')
        issues_analysis = issues_analyzer.analyze(best_code) if best_code else {'issues_text': 'No code to analyze'}

        return {
            'total_models_tested': len(results),
            'successful_evaluations': len(successful_results),
            'failed_evaluations': len(results) - len(successful_results),
            'best_model': best_result['model'],
            'best_score': best_result['overall_score'],
            'best_generated_code': best_code,
            'potential_issues': issues_analysis.get('issues_text', 'No analysis available')
        }
