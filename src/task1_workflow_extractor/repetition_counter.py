# src/task1_workflow_extractor/repetition_counter.py
from typing import List
from datetime import date
from ..models.workflow_schema import WorkflowPattern

class RepetitionCounter:
    def __init__(self, date_range: List[date]):
        self.date_range = date_range
        
    def count_repetitions(self, patterns: List[WorkflowPattern]) -> List[WorkflowPattern]:
        """Count repetitions for all patterns"""
        for pattern in patterns:
            pattern.calculate_repetitions(self.date_range)
        return patterns
    
    def filter_high_value_patterns(self, patterns: List[WorkflowPattern], 
                                     min_occurrences: int = 2) -> List[WorkflowPattern]:
        """Filter patterns with high repetition value"""
        return [p for p in patterns if p.repetition_counts.get('total_occurrences', 0) >= min_occurrences]
