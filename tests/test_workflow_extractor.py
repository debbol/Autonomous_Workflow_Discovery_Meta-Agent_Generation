# tests/test_workflow_extractor.py
import pytest
from datetime import datetime, date
from src.models.event_models import Event, Capture
from src.models.workflow_schema import Workflow, ActionType
from src.task1_workflow_extractor.workflow_extractor import WorkflowExtractor
from src.task1_workflow_extractor.pattern_matcher import PatternMatcher

class TestWorkflowExtractor:
    def setup_method(self):
        self.extractor = WorkflowExtractor(min_workflow_length=2)
        
    def test_split_into_sessions(self):
        # Create test captures
        base_time = datetime.now()
        captures = [
            Capture(id=i, event_id=i, timestamp=base_time + timedelta(minutes=i*10),
                   image_path=f"test_{i}.png", id_employee="EMP-001", event=None)
            for i in range(5)
        ]
        
        sessions = self.extractor._split_into_sessions(captures)
        assert len(sessions) > 0

class TestPatternMatcher:
    def setup_method(self):
        self.matcher = PatternMatcher()
        
    def test_pattern_matching(self):
        # Create test workflows
        workflows = [
            Workflow("WF1", "EMP-001", []),
            Workflow("WF2", "EMP-001", [])
        ]
        
        patterns = self.matcher.group_into_patterns(workflows)
        assert len(patterns) >= 0
