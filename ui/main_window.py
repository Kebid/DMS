"""
Main Window for Dental Clinic Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
import logging

from .patient_frame import PatientFrame
from .appointment_frame import AppointmentFrame
from .treatment_frame import TreatmentFrame
from .dashboard_frame import DashboardFrame

class MainWindow:
    """Main application window"""
    
    def __init__(self, root: tk.Tk, db_manager, current_user: dict):
        """Initialize the main window"""
        self.root = root
        self.db_manager = db_manager
        self.current_user = current_user
        self.logger = logging.getLogger(__name__)
        
        # Current frame reference
        self.current_frame: Optional[tk.Frame] = None
        
        self.setup_ui()
        self.show_dashboard()
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Configure the main window
        self.root.configure(bg='#f0f0f0')
        
        # Create main container
        self.main_container = tk.Frame(self.root, bg='#f0f0f0')
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create header
        self.create_header()
        
        # Create navigation
        self.create_navigation()
        
        # Create content area
        self.create_content_area()
        
        # Create status bar
        self.create_status_bar()
    
    def create_header(self):
        """Create the application header"""
        header_frame = tk.Frame(self.main_container, bg='#2c3e50', height=60)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="Dental Clinic Management System",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # User info
        user_info = f"Welcome, {self.current_user['username'].title()} ({self.current_user['role'].title()})"
        user_label = tk.Label(
            header_frame,
            text=user_info,
            font=('Arial', 10),
            fg='white',
            bg='#2c3e50'
        )
        user_label.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Logout button
        logout_btn = tk.Button(
            header_frame,
            text="Logout",
            command=self.logout,
            font=('Arial', 9),
            bg='#e74c3c',
            fg='white',
            bd=0,
            padx=10,
            pady=2,
            cursor='hand2'
        )
        logout_btn.pack(side=tk.RIGHT, padx=(0, 10), pady=15)
    
    def create_navigation(self):
        """Create the navigation menu"""
        nav_frame = tk.Frame(self.main_container, bg='#34495e', height=50)
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        nav_frame.pack_propagate(False)
        
        # Navigation buttons based on user role
        nav_buttons = self.get_navigation_buttons()
        
        for i, (text, command) in enumerate(nav_buttons):
            btn = tk.Button(
                nav_frame,
                text=text,
                command=command,
                font=('Arial', 10),
                bg='#34495e',
                fg='white',
                bd=0,
                padx=20,
                pady=10,
                activebackground='#2c3e50',
                activeforeground='white',
                cursor='hand2'
            )
            btn.pack(side=tk.LEFT, padx=5)
            
            # Bind hover events
            btn.bind('<Enter>', lambda e, b=btn: self.on_nav_hover(b, True))
            btn.bind('<Leave>', lambda e, b=btn: self.on_nav_hover(b, False))
    
    def create_content_area(self):
        """Create the main content area"""
        self.content_frame = tk.Frame(self.main_container, bg='white', relief=tk.RAISED, bd=1)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
    
    def create_status_bar(self):
        """Create the status bar"""
        status_frame = tk.Frame(self.main_container, bg='#ecf0f1', height=25)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            font=('Arial', 9),
            fg='#2c3e50',
            bg='#ecf0f1'
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Clock
        self.clock_label = tk.Label(
            status_frame,
            text="",
            font=('Arial', 9),
            fg='#2c3e50',
            bg='#ecf0f1'
        )
        self.clock_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Start clock update
        self.update_clock()
    
    def on_nav_hover(self, button: tk.Button, entering: bool):
        """Handle navigation button hover events"""
        if entering:
            button.configure(bg='#2c3e50')
        else:
            button.configure(bg='#34495e')
    
    def update_clock(self):
        """Update the clock display"""
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.configure(text=current_time)
        self.root.after(1000, self.update_clock)
    
    def clear_content(self):
        """Clear the current content frame"""
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None
    
    def show_dashboard(self):
        """Show the dashboard frame"""
        self.clear_content()
        self.current_frame = DashboardFrame(self.content_frame, self.db_manager, self.current_user)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.status_label.configure(text="Dashboard loaded")
        self.logger.info("Dashboard displayed")
    
    def show_patients(self):
        """Show the patients frame"""
        self.clear_content()
        self.current_frame = PatientFrame(self.content_frame, self.db_manager)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.status_label.configure(text="Patient management loaded")
        self.logger.info("Patient management displayed")
    
    def show_appointments(self):
        """Show the appointments frame"""
        self.clear_content()
        self.current_frame = AppointmentFrame(self.content_frame, self.db_manager)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.status_label.configure(text="Appointment management loaded")
        self.logger.info("Appointment management displayed")
    
    def show_treatments(self):
        """Show the treatments frame"""
        self.clear_content()
        self.current_frame = TreatmentFrame(self.content_frame, self.db_manager)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.status_label.configure(text="Treatment management loaded")
        self.logger.info("Treatment management displayed")
    
    def show_reports(self):
        """Show the reports frame (placeholder)"""
        self.clear_content()
        
        # Create a simple reports frame
        reports_frame = tk.Frame(self.content_frame, bg='white')
        reports_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            reports_frame,
            text="Reports",
            font=('Arial', 16, 'bold'),
            bg='white'
        )
        title_label.pack(pady=20)
        
        # Placeholder content
        placeholder_label = tk.Label(
            reports_frame,
            text="Reports functionality coming soon...",
            font=('Arial', 12),
            bg='white',
            fg='#7f8c8d'
        )
        placeholder_label.pack(pady=50)
        
        self.current_frame = reports_frame
        self.status_label.configure(text="Reports loaded")
        self.logger.info("Reports displayed")
    
    def show_error(self, message: str):
        """Show an error message"""
        messagebox.showerror("Error", message)
        self.logger.error(f"Error displayed: {message}")
    
    def show_info(self, message: str):
        """Show an info message"""
        messagebox.showinfo("Information", message)
        self.logger.info(f"Info displayed: {message}")
    
    def show_warning(self, message: str):
        """Show a warning message"""
        messagebox.showwarning("Warning", message)
        self.logger.warning(f"Warning displayed: {message}")
    
    def get_navigation_buttons(self):
        """Get navigation buttons based on user role"""
        role = self.current_user.get('role', 'staff')
        
        # Base navigation for all users
        nav_buttons = [
            ("Dashboard", self.show_dashboard),
        ]
        
        # Role-specific navigation
        if role in ['admin', 'receptionist']:
            nav_buttons.extend([
                ("Patients", self.show_patients),
                ("Appointments", self.show_appointments),
            ])
        
        if role in ['admin', 'dentist', 'doctor']:
            nav_buttons.extend([
                ("Treatments", self.show_treatments),
            ])
        
        if role == 'admin':
            nav_buttons.extend([
                ("Users", self.show_users),
                ("Reports", self.show_reports),
            ])
        
        return nav_buttons
    
    def logout(self):
        """Logout and return to login screen"""
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            self.logger.info(f"User {self.current_user['username']} logged out")
            self.root.destroy()
            
            # Restart login window
            from .login_window import LoginWindow
            login = LoginWindow(self.db_manager)
            login.run()
    
    def show_users(self):
        """Show users management (admin only)"""
        self.clear_content()
        from .user_frame import UserFrame
        self.current_frame = UserFrame(self.content_frame, self.db_manager, self.current_user)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.status_label.configure(text="User management loaded")
        self.logger.info("User management displayed") 