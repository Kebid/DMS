"""
Appointment model for Dental Clinic Management System
"""

from datetime import date, time
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum

class AppointmentStatus(Enum):
    """Appointment status enumeration"""
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

@dataclass
class Appointment:
    """Appointment data model"""
    
    id: Optional[int] = None
    patient_id: int = 0
    appointment_date: date = None
    appointment_time: time = None
    duration: int = 60  # Duration in minutes
    treatment_type: str = ""
    notes: str = ""
    status: AppointmentStatus = AppointmentStatus.SCHEDULED
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    # Additional fields for display purposes
    patient_name: str = ""
    
    @property
    def end_time(self) -> Optional[time]:
        """Calculate appointment end time"""
        if self.appointment_time:
            total_minutes = self.appointment_time.hour * 60 + self.appointment_time.minute + self.duration
            hours = total_minutes // 60
            minutes = total_minutes % 60
            return time(hour=hours, minute=minutes)
        return None
    
    @property
    def is_past(self) -> bool:
        """Check if appointment is in the past"""
        if self.appointment_date:
            return self.appointment_date < date.today()
        return False
    
    @property
    def is_today(self) -> bool:
        """Check if appointment is today"""
        if self.appointment_date:
            return self.appointment_date == date.today()
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert appointment to dictionary"""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'appointment_time': self.appointment_time.isoformat() if self.appointment_time else None,
            'duration': self.duration,
            'treatment_type': self.treatment_type,
            'notes': self.notes,
            'status': self.status.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'patient_name': self.patient_name
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Appointment':
        """Create appointment from dictionary"""
        # Convert date string to date object if present
        appointment_date = None
        if data.get('appointment_date'):
            try:
                appointment_date = date.fromisoformat(data['appointment_date'])
            except ValueError:
                pass
        
        # Convert time string to time object if present
        appointment_time = None
        if data.get('appointment_time'):
            try:
                appointment_time = time.fromisoformat(data['appointment_time'])
            except ValueError:
                pass
        
        # Convert status string to enum
        status = AppointmentStatus.SCHEDULED
        if data.get('status'):
            try:
                status = AppointmentStatus(data['status'])
            except ValueError:
                pass
        
        return cls(
            id=data.get('id'),
            patient_id=data.get('patient_id', 0),
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            duration=data.get('duration', 60),
            treatment_type=data.get('treatment_type', ''),
            notes=data.get('notes', ''),
            status=status,
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            patient_name=data.get('patient_name', '')
        )
    
    def validate(self) -> list:
        """Validate appointment data and return list of errors"""
        errors = []
        
        if not self.patient_id:
            errors.append("Patient is required")
        
        if not self.appointment_date:
            errors.append("Appointment date is required")
        elif self.appointment_date < date.today():
            errors.append("Appointment date cannot be in the past")
        
        if not self.appointment_time:
            errors.append("Appointment time is required")
        
        if self.duration <= 0:
            errors.append("Duration must be greater than 0")
        
        if self.duration > 480:  # 8 hours
            errors.append("Duration cannot exceed 8 hours")
        
        return errors
    
    def get_status_color(self) -> str:
        """Get color for appointment status display"""
        status_colors = {
            AppointmentStatus.SCHEDULED: "#007bff",  # Blue
            AppointmentStatus.CONFIRMED: "#28a745",  # Green
            AppointmentStatus.IN_PROGRESS: "#ffc107",  # Yellow
            AppointmentStatus.COMPLETED: "#6c757d",  # Gray
            AppointmentStatus.CANCELLED: "#dc3545",  # Red
            AppointmentStatus.NO_SHOW: "#dc3545"  # Red
        }
        return status_colors.get(self.status, "#6c757d")
    
    def get_status_display_name(self) -> str:
        """Get display name for appointment status"""
        status_names = {
            AppointmentStatus.SCHEDULED: "Scheduled",
            AppointmentStatus.CONFIRMED: "Confirmed",
            AppointmentStatus.IN_PROGRESS: "In Progress",
            AppointmentStatus.COMPLETED: "Completed",
            AppointmentStatus.CANCELLED: "Cancelled",
            AppointmentStatus.NO_SHOW: "No Show"
        }
        return status_names.get(self.status, "Unknown") 