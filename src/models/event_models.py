# src/models/event_models.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
import json

@dataclass
class Event:
    id: int
    timestamp: datetime
    app_name: str
    window_title: str
    event_type: str  # Click, Type, Scroll, App Switch, Copy/Paste
    url: Optional[str]
    clipboard_content: Optional[str]
    id_employee: str
    x_coord: Optional[int]
    y_coord: Optional[int]
    typed_text: Optional[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'app_name': self.app_name,
            'window_title': self.window_title,
            'event_type': self.event_type,
            'url': self.url,
            'clipboard_content': self.clipboard_content,
            'id_employee': self.id_employee,
            'coordinates': {'x': self.x_coord, 'y': self.y_coord} if self.x_coord else None,
            'typed_text': self.typed_text
        }

@dataclass
class Capture:
    id: int
    event_id: int
    timestamp: datetime
    image_path: str
    id_employee: str
    event: Optional[Event] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'event_id': self.event_id,
            'timestamp': self.timestamp.isoformat(),
            'image_path': self.image_path,
            'id_employee': self.id_employee,
            'event': self.event.to_dict() if self.event else None
        }
