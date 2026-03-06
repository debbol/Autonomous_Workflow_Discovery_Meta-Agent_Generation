# src/models/workflow_schema.py
from typing import List, Dict, Any, Set, Optional
from typing import List, Dict, Any, Set
from datetime import date, datetime
from enum import Enum
from collections import defaultdict
import hashlib
import json

class ActionType(Enum):
    CLICK = "click"
    TYPE = "type"
    SCROLL = "scroll"
    APP_SWITCH = "app_switch"
    COPY = "copy"
    PASTE = "paste"
    NAVIGATE = "navigate"

class WorkflowStep:
    def __init__(self, action_type: ActionType, details: Dict[str, Any], 
                 screenshot_path: Optional[str] = None):
        self.action_type = action_type
        self.details = details
        self.screenshot_path = screenshot_path
        self.timestamp = details.get('timestamp')
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'action_type': self.action_type.value,
            'details': self.details,
            'screenshot_path': self.screenshot_path,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    def to_executable_code(self) -> str:
        """Convert step to executable Python code"""
        if self.action_type == ActionType.CLICK:
            return f"pyautogui.click({self.details.get('x', 0)}, {self.details.get('y', 0)})"
        elif self.action_type == ActionType.TYPE:
            return f"pyautogui.write({repr(self.details.get('text', ''))})"
        elif self.action_type == ActionType.APP_SWITCH:
            return f"# Switch to app: {self.details.get('app_name', '')}\nsubprocess.run(['open', '-a', {repr(self.details.get('app_name', ''))}])"
        elif self.action_type == ActionType.COPY:
            return "pyautogui.hotkey('command', 'c')"
        elif self.action_type == ActionType.PASTE:
            return "pyautogui.hotkey('command', 'v')"
        elif self.action_type == ActionType.NAVIGATE:
            return f"pyautogui.write({repr(self.details.get('url', ''))})\npyautogui.press('enter')"
        return "# Unsupported action type"

class Workflow:
    def __init__(self, workflow_id: str, employee_id: str, steps: List[WorkflowStep]):
        self.workflow_id = workflow_id
        self.employee_id = employee_id
        self.steps = steps
        self.pattern_signature = self._generate_signature()
        
    def _generate_signature(self) -> str:
        """Generate a signature for pattern matching"""
        action_sequence = [step.action_type.value for step in self.steps]
        return "->".join(action_sequence)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'workflow_id': self.workflow_id,
            'employee_id': self.employee_id,
            'pattern_signature': self.pattern_signature,
            'steps': [step.to_dict() for step in self.steps],
            'step_count': len(self.steps)
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, default=str)

class WorkflowPattern:
    def __init__(self, pattern_id: str, signature: str, 
                 workflows: List[Workflow], employee_id: str):
        self.pattern_id = pattern_id
        self.signature = signature
        self.workflows = workflows
        self.employee_id = employee_id
        self.repetition_counts = {}
        
    def calculate_repetitions(self, date_range: List[date]):
        """Calculate repetition counts for different timeframes"""
        # Group by date
        by_date = defaultdict(list)
        for wf in self.workflows:
            if wf.steps and wf.steps[0].timestamp:
                wf_date = wf.steps[0].timestamp.date()
                by_date[wf_date].append(wf)
        
        # Daily counts
        daily_counts = {}
        for d in date_range:
            daily_counts[d.isoformat()] = len(by_date.get(d, []))
        
        # Persistence across days
        dates_with_workflow = set(by_date.keys())
        
        self.repetition_counts = {
            'daily': daily_counts,
            '2_day_persistence': self._check_persistence(dates_with_workflow, 2),
            '3_day_persistence': self._check_persistence(dates_with_workflow, 3),
            '4_day_persistence': self._check_persistence(dates_with_workflow, 4),
            'total_occurrences': len(self.workflows),
            'unique_days': len(dates_with_workflow)
        }
        
    def _check_persistence(self, dates: Set[date], days_required: int) -> bool:
        """Check if pattern appears across N days (non-consecutive)"""
        return len(dates) >= days_required
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'pattern_id': self.pattern_id,
            'signature': self.signature,
            'employee_id': self.employee_id,
            'repetition_counts': self.repetition_counts,
            'sample_workflow': self.workflows[0].to_dict() if self.workflows else None,
            'occurrences': len(self.workflows)
        }
