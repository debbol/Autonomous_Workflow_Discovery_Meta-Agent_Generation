# src/task1_workflow_extractor/pattern_matcher.py
from typing import List, Set
from ..models.workflow_schema import Workflow, WorkflowPattern
import hashlib

class PatternMatcher:
    def __init__(self, similarity_threshold: float = 0.8):
        self.similarity_threshold = similarity_threshold
        
    def group_into_patterns(self, workflows: List[Workflow]) -> List[WorkflowPattern]:
        """Group similar workflows into patterns"""
        patterns = []
        used_workflows = set()
        
        for i, wf1 in enumerate(workflows):
            if i in used_workflows:
                continue
                
            pattern_workflows = [wf1]
            used_workflows.add(i)
            
            # Find similar workflows
            for j, wf2 in enumerate(workflows):
                if j in used_workflows:
                    continue
                    
                if self._are_similar(wf1, wf2):
                    pattern_workflows.append(wf2)
                    used_workflows.add(j)
                    
            if pattern_workflows:
                # Generate pattern ID
                pattern_id = hashlib.md5(
                    wf1.pattern_signature.encode()
                ).hexdigest()[:8]
                
                pattern = WorkflowPattern(
                    pattern_id=f"P_{pattern_id}",
                    signature=wf1.pattern_signature,
                    workflows=pattern_workflows,
                    employee_id=wf1.employee_id
                )
                patterns.append(pattern)
                
        return patterns
    
    def _are_similar(self, wf1: Workflow, wf2: Workflow) -> bool:
        """Check if two workflows are similar"""
        # Compare signatures first (fast)
        if wf1.pattern_signature != wf2.pattern_signature:
            return False
            
        # Compare step details if needed
        if len(wf1.steps) != len(wf2.steps):
            return False
            
        # Calculate similarity score
        similar_steps = 0
        for s1, s2 in zip(wf1.steps, wf2.steps):
            if self._steps_similar(s1, s2):
                similar_steps += 1
                
        similarity = similar_steps / len(wf1.steps) if wf1.steps else 0
        return similarity >= self.similarity_threshold
    
    def _steps_similar(self, step1, step2) -> bool:
        """Check if two steps are similar"""
        if step1.action_type != step2.action_type:
            return False
            
        # Compare app names if available
        if step1.details.get('app_name') != step2.details.get('app_name'):
            return False
            
        return True
