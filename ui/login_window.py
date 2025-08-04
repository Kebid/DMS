"""
Login Window for Dental Clinic Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import logging
from typing import Optional, Dict, Any

class LoginWindow:
    """Login window with authentication"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)
        self.current_user = None
        
        # Create login window
        self.root = tk.Tk()
        self.setup_login_window()
        
    def setup_login_window(self):
        """Setup the login window interface"""
        # Configure window
        self.root.title("Dental Clinic Management System - Login")
        self.root.geometry("450x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
        
        # Center window on screen
        self.center_window()
        
        # Create main container
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Logo/Title section
        self.create_header_section(main_container)
        
        # Login form section
        self.create_login_form(main_container)
        
        # Help section
        self.create_help_section(main_container)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.login())
        
        # Focus on username field
        self.username_entry.focus()
    
    def create_header_section(self, parent):
        """Create the header section with logo and title"""
        # Logo
        logo_label = tk.Label(
            parent,
            text="🦷",
            font=('Arial', 48),
            bg='#f0f0f0'
        )
        logo_label.pack(pady=(0, 10))
        
        # Title
        title_label = tk.Label(
            parent,
            text="Dental Clinic",
            font=('Arial', 24, 'bold'),
            fg='#2c3e50',
            bg='#f0f0f0'
        )
        title_label.pack(pady=(0, 5))
        
        # Subtitle
        subtitle_label = tk.Label(
            parent,
            text="Management System",
            font=('Arial', 14),
            fg='#7f8c8d',
            bg='#f0f0f0'
        )
        subtitle_label.pack(pady=(0, 30))
    
    def create_login_form(self, parent):
        """Create the login form section"""
        # Form container
        form_container = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=2)
        form_container.pack(fill=tk.X, pady=20)
        
        # Form title
        form_title = tk.Label(
            form_container,
            text="Login",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        form_title.pack(pady=20)
        
        # Username field
        username_frame = tk.Frame(form_container, bg='white')
        username_frame.pack(fill=tk.X, padx=30, pady=10)
        
        username_label = tk.Label(
            username_frame,
            text="Username:",
            font=('Arial', 10, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        username_label.pack(anchor=tk.W)
        
        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(
            username_frame,
            textvariable=self.username_var,
            font=('Arial', 12),
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightcolor='#3498db'
        )
        self.username_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Password field
        password_frame = tk.Frame(form_container, bg='white')
        password_frame.pack(fill=tk.X, padx=30, pady=10)
        
        password_label = tk.Label(
            password_frame,
            text="Password:",
            font=('Arial', 10, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        password_label.pack(anchor=tk.W)
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            password_frame,
            textvariable=self.password_var,
            font=('Arial', 12),
            show="*",
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightcolor='#3498db'
        )
        self.password_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Login button
        button_frame = tk.Frame(form_container, bg='white')
        button_frame.pack(fill=tk.X, padx=30, pady=20)
        
        self.login_button = tk.Button(
            button_frame,
            text="Login",
            command=self.login,
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            bd=0,
            padx=30,
            pady=12,
            cursor='hand2',
            activebackground='#2980b9',
            activeforeground='white'
        )
        self.login_button.pack(fill=tk.X)
        
        # Status label
        self.status_label = tk.Label(
            form_container,
            text="",
            font=('Arial', 10),
            fg='#e74c3c',
            bg='white'
        )
        self.status_label.pack(pady=(10, 20))
    
    def create_help_section(self, parent):
        """Create the help section with sample credentials"""
        help_frame = tk.Frame(parent, bg='#f0f0f0')
        help_frame.pack(fill=tk.X, pady=10)
        
        help_title = tk.Label(
            help_frame,
            text="Sample Credentials:",
            font=('Arial', 10, 'bold'),
            fg='#2c3e50',
            bg='#f0f0f0'
        )
        help_title.pack(pady=(0, 5))
        
        credentials_text = """Doctor: doctor / doctor123
Receptionist: receptionist / recep123"""
        
        credentials_label = tk.Label(
            help_frame,
            text=credentials_text,
            font=('Arial', 9),
            fg='#7f8c8d',
            bg='#f0f0f0',
            justify=tk.LEFT
        )
        credentials_label.pack()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self):
        """Login function - called when login button is clicked"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        # Clear status
        self.status_label.config(text="")
        
        # Validate input
        if not username or not password:
            self.status_label.config(text="Please enter both username and password")
            return
        
        try:
            # Use the new user manager for authentication
            from database.user_manager import UserManager
            user_manager = UserManager("clinic.db")
            user = user_manager.authenticate_user(username, password)
            
            if not user:
                self.status_label.config(text="Invalid username or password")
                self.logger.warning(f"Failed login attempt for username: {username}")
                return
            
            # Store current user
            self.current_user = user
            
            # Log successful login
            self.logger.info(f"Successful login for user: {username} (role: {user['role']})")
            
            # Close login window and open appropriate dashboard
            self.root.destroy()
            self.open_dashboard(user)
            
        except Exception as e:
            self.logger.error(f"Authentication error: {e}")
            self.status_label.config(text="Login error. Please try again.")
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username from database"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            self.logger.error(f"Error getting user by username: {e}")
            raise
    
    def update_last_login(self, user_id: int):
        """Update user's last login timestamp"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users 
                    SET last_login = CURRENT_TIMESTAMP 
                    WHERE id = ?
                ''', (user_id,))
                conn.commit()
        except Exception as e:
            self.logger.error(f"Error updating last login: {e}")
            # Don't raise - this is not critical for login
    
    def open_dashboard(self, user: Dict[str, Any]):
        """Open appropriate dashboard based on user role"""
        from .main_window import MainWindow
        
        # Create main application window
        root = tk.Tk()
        app = MainWindow(root, self.db_manager, user)
        
        # Set window properties
        root.title(f"Dental Clinic Management System - {user['first_name']} {user['last_name']}")
        root.geometry("1200x800")
        root.minsize(800, 600)
        
        # Center the window on screen
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Start the main event loop
        root.mainloop()
    
    def run(self):
        """Start the login window"""
        self.root.mainloop()
    
    def create_default_admin(self):
        """Create default users if no users exist"""
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if any users exist
                cursor.execute('SELECT COUNT(*) FROM users')
                user_count = cursor.fetchone()[0]
                
                if user_count == 0:
                    # Create default users
                    default_users = [
                        {
                            'username': 'admin',
                            'password_hash': self.hash_password('admin123'),
                            'first_name': 'System',
                            'last_name': 'Administrator',
                            'email': 'admin@dentalclinic.com',
                            'role': 'admin'
                        },
                        {
                            'username': 'dentist',
                            'password_hash': self.hash_password('dentist123'),
                            'first_name': 'Dr. Sarah',
                            'last_name': 'Johnson',
                            'email': 'sarah.johnson@dentalclinic.com',
                            'role': 'dentist'
                        },
                        {
                            'username': 'receptionist',
                            'password_hash': self.hash_password('reception123'),
                            'first_name': 'Maria',
                            'last_name': 'Garcia',
                            'email': 'maria.garcia@dentalclinic.com',
                            'role': 'receptionist'
                        }
                    ]
                    
                    for user_data in default_users:
                        cursor.execute('''
                            INSERT INTO users (username, password_hash, first_name, last_name, email, role)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (
                            user_data['username'],
                            user_data['password_hash'],
                            user_data['first_name'],
                            user_data['last_name'],
                            user_data['email'],
                            user_data['role']
                        ))
                    
                    conn.commit()
                    self.logger.info("Default users created:")
                    self.logger.info("- Admin: admin/admin123")
                    self.logger.info("- Dentist: dentist/dentist123")
                    self.logger.info("- Receptionist: receptionist/reception123")
                    
        except Exception as e:
            self.logger.error(f"Error creating default users: {e}")
            raise 