# src/task1_workflow_extractor/workflow_extractor.py
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from ..models.event_models import Capture, Event
from ..models.workflow_schema import Workflow, WorkflowStep, ActionType
import hashlib

class WorkflowExtractor:
    def __init__(self, min_workflow_length: int = 3, 
                 max_pause_seconds: int = 30,
                 use_screenshots: bool = True):
        self.min_workflow_length = min_workflow_length
        self.max_pause_seconds = max_pause_seconds
        self.use_screenshots = use_screenshots
        
    def extract_workflows(self, captures: List[Capture], 
                          employee_id: str) -> List[Workflow]:
        """Extract workflows from capture sequence"""
        if not captures:
            return []
            
        workflows = []
        
        # Group captures into sessions based on time gaps
        sessions = self._split_into_sessions(captures)
        
        for session_idx, session in enumerate(sessions):
            # Extract workflows from each session
            session_workflows = self._extract_from_session(session, employee_id, session_idx)
            workflows.extend(session_workflows)
            
        return workflows
    
    def _split_into_sessions(self, captures: List[Capture]) -> List[List[Capture]]:
        """Split captures into sessions based on time gaps"""
        sessions = []
        current_session = []
        
        for i, capture in enumerate(captures):
            if i == 0:
                current_session.append(capture)
                continue
                
            time_gap = (capture.timestamp - captures[i-1].timestamp).total_seconds()
            
            if time_gap > self.max_pause_seconds * 60:  # Convert to seconds
                # New session
                if len(current_session) >= self.min_workflow_length:
                    sessions.append(current_session)
                current_session = [capture]
            else:
                current_session.append(capture)
                
        # Add last session
        if len(current_session) >= self.min_workflow_length:
            sessions.append(current_session)
            
        return sessions
    
    def _extract_from_session(self, session: List[Capture], 
                               employee_id: str, 
                               session_idx: int) -> List[Workflow]:
        """Extract workflows from a session"""
        workflows = []
        
        # Use sliding window to detect potential workflows
        window_size = self.min_workflow_length
        
        for i in range(len(session) - window_size + 1):
            # Try different window sizes
            for size in range(window_size, min(len(session) - i + 1, 10)):
                window = session[i:i+size]
                
                # Check if this window forms a coherent workflow
                if self._is_coherent_workflow(window):
                    workflow = self._create_workflow(window, employee_id, 
                                                      f"{session_idx}_{i}")
                    workflows.append(workflow)
                    
        return workflows
    
    def _is_coherent_workflow(self, captures: List[Capture]) -> bool:
        """Check if a sequence of captures forms a coherent workflow"""
        if len(captures) < self.min_workflow_length:
            return False
            
        # Check if all captures have associated events
        if not all(c.event for c in captures):
            return False
            
        # Check if the sequence has a logical flow (e.g., copy -> paste)
        events = [c.event for c in captures if c.event]
        
        # Look for common workflow patterns
        event_types = [e.event_type for e in events]
        
        # Example: Copy-Paste workflow
        if 'Copy' in event_types and 'Paste' in event_types:
            copy_idx = event_types.index('Copy')
            paste_idx = event_types.index('Paste') if 'Paste' in event_types else -1
            if paste_idx > copy_idx:
                return True
                
        # Browser navigation workflow
        if any(e.url for e in events):
            return True
            
        return True  # Default to True for now
    
    def _create_workflow(self, captures: List[Capture], 
                          employee_id: str, 
                          workflow_suffix: str) -> Workflow:
        """Create a Workflow object from captures"""
        steps = []
        
        for capture in captures:
            if not capture.event:
                continue
                
            event = capture.event
            
            # Map event type to ActionType
            action_type = self._map_event_to_action(event.event_type)
            
            # Extract details based on event type
            details = self._extract_event_details(event)
            details['timestamp'] = capture.timestamp
            
            # Include screenshot path if available
            screenshot_path = capture.image_path if self.use_screenshots else None
            
            step = WorkflowStep(action_type, details, screenshot_path)
            steps.append(step)
            
        # Generate workflow ID
        workflow_id = f"WF_{employee_id}_{workflow_suffix}"
        workflow_id = hashlib.md5(workflow_id.encode()).hexdigest()[:12]
        
        return Workflow(workflow_id, employee_id, steps)
    
    def _map_event_to_action(self, event_type: str) -> ActionType:
        """Map database event type to ActionType enum"""
        mapping = {
            'Click': ActionType.CLICK,
            'Type': ActionType.TYPE,
            'Scroll': ActionType.SCROLL,
            'App Switch': ActionType.APP_SWITCH,
            'Copy': ActionType.COPY,
            'Paste': ActionType.PASTE,
            'Navigate': ActionType.NAVIGATE
        }
        return mapping.get(event_type, ActionType.CLICK)
    
    def _extract_event_details(self, event: Event) -> Dict[str, Any]:
        """Extract relevant details from event"""
        details = {
            'app_name': event.app_name,
            'window_title': event.window_title,
            'event_type': event.event_type
        }
        
        if event.event_type == 'Click' and event.x_coord and event.y_coord:
            details['x'] = event.x_coord
            details['y'] = event.y_coord
        elif event.event_type == 'Type' and event.typed_text:
            details['text'] = event.typed_text
        elif event.event_type == 'Copy':
            details['content'] = event.clipboard_content
        elif event.event_type == 'Paste':
            details['content'] = event.clipboard_content
        elif event.url:
            details['url'] = event.url
            
        return details
