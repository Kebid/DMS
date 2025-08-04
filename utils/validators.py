"""
Validation utilities for Dental Clinic Management System
"""

import re
from datetime import date, datetime
from typing import Optional

def validate_email(email: str) -> bool:
    """
    Validate email address format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not email:
        return True  # Empty email is allowed
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """
    Validate phone number format
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not phone:
        return True  # Empty phone is allowed
    
    # Remove common separators
    clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check if it's a valid phone number (basic validation)
    pattern = r'^[\+]?[1-9][\d]{0,15}$'
    return bool(re.match(pattern, clean_phone))

def validate_date(date_str: str) -> bool:
    """
    Validate date string format (YYYY-MM-DD)
    
    Args:
        date_str: Date string to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not date_str:
        return True  # Empty date is allowed
    
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_time(time_str: str) -> bool:
    """
    Validate time string format (HH:MM)
    
    Args:
        time_str: Time string to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not time_str:
        return True  # Empty time is allowed
    
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

def validate_positive_number(value: str, field_name: str = "Value") -> tuple[bool, Optional[str]]:
    """
    Validate that a string represents a positive number
    
    Args:
        value: String value to validate
        field_name: Name of the field for error message
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return False, f"{field_name} is required"
    
    try:
        num_value = float(value)
        if num_value < 0:
            return False, f"{field_name} cannot be negative"
        return True, None
    except ValueError:
        return False, f"{field_name} must be a valid number"

def validate_positive_integer(value: str, field_name: str = "Value") -> tuple[bool, Optional[str]]:
    """
    Validate that a string represents a positive integer
    
    Args:
        value: String value to validate
        field_name: Name of the field for error message
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value:
        return False, f"{field_name} is required"
    
    try:
        num_value = int(value)
        if num_value <= 0:
            return False, f"{field_name} must be greater than 0"
        return True, None
    except ValueError:
        return False, f"{field_name} must be a valid integer"

def validate_required(value: str, field_name: str = "Field") -> tuple[bool, Optional[str]]:
    """
    Validate that a required field is not empty
    
    Args:
        value: String value to validate
        field_name: Name of the field for error message
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value or not value.strip():
        return False, f"{field_name} is required"
    return True, None

def validate_date_range(start_date: str, end_date: str) -> tuple[bool, Optional[str]]:
    """
    Validate that start date is before end date
    
    Args:
        start_date: Start date string (YYYY-MM-DD)
        end_date: End date string (YYYY-MM-DD)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        if start > end:
            return False, "Start date cannot be after end date"
        
        return True, None
    except ValueError:
        return False, "Invalid date format"

def validate_appointment_time(appointment_date: str, appointment_time: str) -> tuple[bool, Optional[str]]:
    """
    Validate appointment date and time
    
    Args:
        appointment_date: Appointment date string (YYYY-MM-DD)
        appointment_time: Appointment time string (HH:MM)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        apt_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
        apt_time = datetime.strptime(appointment_time, '%H:%M').time()
        
        # Check if appointment is in the past
        now = datetime.now()
        if apt_date < now.date():
            return False, "Appointment date cannot be in the past"
        
        # If appointment is today, check if time is in the past
        if apt_date == now.date() and apt_time < now.time():
            return False, "Appointment time cannot be in the past"
        
        return True, None
    except ValueError:
        return False, "Invalid date or time format"

def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent SQL injection and other issues
    
    Args:
        text: Input text to sanitize
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', text)
    
    # Trim whitespace
    sanitized = sanitized.strip()
    
    return sanitized

def format_currency(amount: float) -> str:
    """
    Format amount as currency
    
    Args:
        amount: Amount to format
        
    Returns:
        Formatted currency string
    """
    return f"${amount:.2f}"

def format_phone(phone: str) -> str:
    """
    Format phone number for display
    
    Args:
        phone: Phone number to format
        
    Returns:
        Formatted phone number
    """
    if not phone:
        return ""
    
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Format based on length
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone  # Return original if can't format 