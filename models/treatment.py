"""
Treatment model for Dental Clinic Management System
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class Treatment:
    """Treatment data model"""
    
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    duration: int = 60  # Duration in minutes
    cost: float = 0.0
    created_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert treatment to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'duration': self.duration,
            'cost': self.cost,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Treatment':
        """Create treatment from dictionary"""
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            description=data.get('description', ''),
            duration=data.get('duration', 60),
            cost=float(data.get('cost', 0.0)),
            created_at=data.get('created_at')
        )
    
    def validate(self) -> list:
        """Validate treatment data and return list of errors"""
        errors = []
        
        if not self.name.strip():
            errors.append("Treatment name is required")
        
        if self.duration <= 0:
            errors.append("Duration must be greater than 0")
        
        if self.duration > 480:  # 8 hours
            errors.append("Duration cannot exceed 8 hours")
        
        if self.cost < 0:
            errors.append("Cost cannot be negative")
        
        return errors 