"""
Patient model for Dental Clinic Management System
"""

from datetime import date
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class Patient:
    """Patient data model"""
    
    id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    date_of_birth: Optional[date] = None
    phone: str = ""
    email: str = ""
    address: str = ""
    emergency_contact: str = ""
    medical_history: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    @property
    def full_name(self) -> str:
        """Get the patient's full name"""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def age(self) -> Optional[int]:
        """Calculate patient's age"""
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert patient to dictionary"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'emergency_contact': self.emergency_contact,
            'medical_history': self.medical_history,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Patient':
        """Create patient from dictionary"""
        # Convert date string to date object if present
        date_of_birth = None
        if data.get('date_of_birth'):
            try:
                date_of_birth = date.fromisoformat(data['date_of_birth'])
            except ValueError:
                pass
        
        return cls(
            id=data.get('id'),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            date_of_birth=date_of_birth,
            phone=data.get('phone', ''),
            email=data.get('email', ''),
            address=data.get('address', ''),
            emergency_contact=data.get('emergency_contact', ''),
            medical_history=data.get('medical_history', ''),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def validate(self) -> list:
        """Validate patient data and return list of errors"""
        errors = []
        
        if not self.first_name.strip():
            errors.append("First name is required")
        
        if not self.last_name.strip():
            errors.append("Last name is required")
        
        if self.phone and not self._is_valid_phone(self.phone):
            errors.append("Invalid phone number format")
        
        if self.email and not self._is_valid_email(self.email):
            errors.append("Invalid email format")
        
        return errors
    
    def _is_valid_phone(self, phone: str) -> bool:
        """Check if phone number is valid"""
        import re
        # Basic phone validation - can be customized based on requirements
        phone_pattern = r'^[\+]?[1-9][\d]{0,15}$'
        return bool(re.match(phone_pattern, phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')))
    
    def _is_valid_email(self, email: str) -> bool:
        """Check if email is valid"""
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email)) 