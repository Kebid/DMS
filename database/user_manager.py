"""
User Management Module for Dental Clinic System
Handles user registration, authentication, and database operations
"""

import sqlite3
import hashlib
import logging
from typing import Optional, Dict, Any

class UserManager:
    """Manages user accounts in the dental clinic system"""
    
    def __init__(self, db_path: str = "clinic.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
    
    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            return conn
        except sqlite3.Error as e:
            self.logger.error(f"Database connection error: {e}")
            raise
    
    def init_users_db(self):
        """Initialize the users table and create default users"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Create users table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL,
                        CHECK (role IN ('doctor', 'receptionist'))
                    )
                ''')
                
                # Check if default users exist
                cursor.execute('SELECT COUNT(*) FROM users')
                user_count = cursor.fetchone()[0]
                
                if user_count == 0:
                    # Register default users
                    self.register_user('doctor', 'doctor123', 'doctor')
                    self.register_user('receptionist', 'recep123', 'receptionist')
                    
                    self.logger.info("Default users created:")
                    self.logger.info("- Doctor: doctor/doctor123")
                    self.logger.info("- Receptionist: receptionist/recep123")
                
                conn.commit()
                self.logger.info("Users database initialized successfully")
                
        except sqlite3.Error as e:
            self.logger.error(f"Error initializing users database: {e}")
            raise
    
    def register_user(self, username: str, password: str, role: str) -> bool:
        """
        Register a new user
        
        Args:
            username: Username for the new user
            password: Plain text password (will be hashed)
            role: User role ('doctor' or 'receptionist')
            
        Returns:
            bool: True if successful, False if username already exists
        """
        try:
            # Hash the password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Insert new user
                cursor.execute('''
                    INSERT INTO users (username, password, role)
                    VALUES (?, ?, ?)
                ''', (username, password_hash, role))
                
                conn.commit()
                self.logger.info(f"User '{username}' registered successfully with role '{role}'")
                return True
                
        except sqlite3.IntegrityError:
            self.logger.warning(f"Username '{username}' already exists")
            return False
        except sqlite3.Error as e:
            self.logger.error(f"Error registering user: {e}")
            raise
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user
        
        Args:
            username: Username to authenticate
            password: Plain text password to verify
            
        Returns:
            dict: User data if authentication successful, None otherwise
        """
        try:
            # Hash the provided password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check credentials
                cursor.execute('''
                    SELECT * FROM users 
                    WHERE username = ? AND password = ?
                ''', (username, password_hash))
                
                row = cursor.fetchone()
                if row:
                    user_data = dict(row)
                    self.logger.info(f"User '{username}' authenticated successfully")
                    return user_data
                else:
                    self.logger.warning(f"Authentication failed for user '{username}'")
                    return None
                    
        except sqlite3.Error as e:
            self.logger.error(f"Error authenticating user: {e}")
            raise
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except sqlite3.Error as e:
            self.logger.error(f"Error getting user by username: {e}")
            raise
    
    def get_all_users(self) -> list:
        """Get all users"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users ORDER BY username')
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            self.logger.error(f"Error getting all users: {e}")
            raise
    
    def update_user_role(self, username: str, new_role: str) -> bool:
        """Update user role"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users 
                    SET role = ? 
                    WHERE username = ?
                ''', (new_role, username))
                
                conn.commit()
                success = cursor.rowcount > 0
                if success:
                    self.logger.info(f"Updated role for user '{username}' to '{new_role}'")
                return success
                
        except sqlite3.Error as e:
            self.logger.error(f"Error updating user role: {e}")
            raise
    
    def delete_user(self, username: str) -> bool:
        """Delete a user"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM users WHERE username = ?', (username,))
                
                conn.commit()
                success = cursor.rowcount > 0
                if success:
                    self.logger.info(f"Deleted user '{username}'")
                return success
                
        except sqlite3.Error as e:
            self.logger.error(f"Error deleting user: {e}")
            raise
    
    def change_password(self, username: str, new_password: str) -> bool:
        """Change user password"""
        try:
            # Hash the new password
            password_hash = hashlib.sha256(new_password.encode()).hexdigest()
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users 
                    SET password = ? 
                    WHERE username = ?
                ''', (password_hash, username))
                
                conn.commit()
                success = cursor.rowcount > 0
                if success:
                    self.logger.info(f"Changed password for user '{username}'")
                return success
                
        except sqlite3.Error as e:
            self.logger.error(f"Error changing password: {e}")
            raise 