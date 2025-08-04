#!/usr/bin/env python3
"""
Dental Clinic Management System
Main entry point for the application
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database_manager import DatabaseManager
from database.user_manager import UserManager
from utils.logger import setup_logger

def init_users_db():
    """Initialize users database with default users"""
    try:
        user_manager = UserManager("clinic.db")
        user_manager.init_users_db()
        return user_manager
    except Exception as e:
        print(f"Error initializing users database: {str(e)}")
        raise

def main():
    """Main function to start the dental clinic management system"""
    try:
        # Setup logging
        logger = setup_logger()
        logger.info("Starting Dental Clinic Management System")
        
        # Initialize users database (Task 3)
        logger.info("Initializing users database...")
        user_manager = init_users_db()
        
        # Initialize main database
        db_manager = DatabaseManager("clinic.db")
        db_manager.initialize_database()
        logger.info("Main database initialized successfully")
        
        # Create and run the login window
        from ui.login_window import LoginWindow
        login = LoginWindow(db_manager)
        
        logger.info("Login window created successfully")
        
        # Start the login window
        login.run()
        
    except Exception as e:
        logger.error(f"Error starting application: {str(e)}")
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 