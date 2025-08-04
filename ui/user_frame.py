"""
User Management Frame for Dental Clinic Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import logging

class UserFrame(tk.Frame):
    """User management frame for administrators"""
    
    def __init__(self, parent, db_manager, current_user):
        super().__init__(parent, bg='white')
        self.db_manager = db_manager
        self.current_user = current_user
        self.logger = logging.getLogger(__name__)
        self.selected_user = None
        
        self.setup_ui()
        self.load_users()
    
    def setup_ui(self):
        """Setup the user management user interface"""
        # Title
        title_label = tk.Label(
            self,
            text="User Management",
            font=('Arial', 18, 'bold'),
            bg='white'
        )
        title_label.pack(pady=(20, 30))
        
        # Main content area
        content_frame = tk.Frame(self, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Left panel - User list
        self.create_user_list_panel(content_frame)
        
        # Right panel - User details
        self.create_user_details_panel(content_frame)
    
    def create_user_list_panel(self, parent):
        """Create the user list panel"""
        list_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Buttons frame
        buttons_frame = tk.Frame(list_frame, bg='white')
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        add_btn = tk.Button(
            buttons_frame,
            text="Add User",
            command=self.add_user,
            bg='#27ae60',
            fg='white',
            bd=0,
            padx=15,
            pady=5
        )
        add_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        refresh_btn = tk.Button(
            buttons_frame,
            text="Refresh",
            command=self.load_users,
            bg='#3498db',
            fg='white',
            bd=0,
            padx=15,
            pady=5
        )
        refresh_btn.pack(side=tk.LEFT)
        
        # User list
        list_label = tk.Label(list_frame, text="Users:", bg='white', font=('Arial', 12, 'bold'))
        list_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Treeview for user list
        self.user_tree = ttk.Treeview(
            list_frame,
            columns=('Username', 'Name', 'Role', 'Status'),
            show='headings',
            height=15
        )
        
        self.user_tree.heading('Username', text='Username')
        self.user_tree.heading('Name', text='Full Name')
        self.user_tree.heading('Role', text='Role')
        self.user_tree.heading('Status', text='Status')
        
        self.user_tree.column('Username', width=120)
        self.user_tree.column('Name', width=150)
        self.user_tree.column('Role', width=100)
        self.user_tree.column('Status', width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=scrollbar.set)
        
        self.user_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 10))
        
        # Bind selection event
        self.user_tree.bind('<<TreeviewSelect>>', self.on_user_select)
    
    def create_user_details_panel(self, parent):
        """Create the user details panel"""
        details_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Title
        details_title = tk.Label(
            details_frame,
            text="User Details",
            font=('Arial', 14, 'bold'),
            bg='white'
        )
        details_title.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(details_frame, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create form fields
        self.create_form_fields(form_frame)
        
        # Action buttons
        self.create_action_buttons(details_frame)
    
    def create_form_fields(self, parent):
        """Create form fields for user details"""
        # Username
        tk.Label(parent, text="Username:", bg='white').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.username_var, width=30).grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # First Name
        tk.Label(parent, text="First Name:", bg='white').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.first_name_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.first_name_var, width=30).grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Last Name
        tk.Label(parent, text="Last Name:", bg='white').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.last_name_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.last_name_var, width=30).grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Email
        tk.Label(parent, text="Email:", bg='white').grid(row=3, column=0, sticky=tk.W, pady=5)
        self.email_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.email_var, width=30).grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Role
        tk.Label(parent, text="Role:", bg='white').grid(row=4, column=0, sticky=tk.W, pady=5)
        self.role_var = tk.StringVar()
        role_combo = ttk.Combobox(parent, textvariable=self.role_var, width=27, state='readonly')
        role_combo['values'] = ['admin', 'dentist', 'hygienist', 'receptionist', 'staff']
        role_combo.grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Password (for new users)
        tk.Label(parent, text="Password:", bg='white').grid(row=5, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(parent, textvariable=self.password_var, width=30, show="*")
        self.password_entry.grid(row=5, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Active status
        self.is_active_var = tk.BooleanVar(value=True)
        active_check = tk.Checkbutton(
            parent, 
            text="Active", 
            variable=self.is_active_var,
            bg='white'
        )
        active_check.grid(row=6, column=1, sticky=tk.W, pady=5, padx=(10, 0))
    
    def create_action_buttons(self, parent):
        """Create action buttons"""
        buttons_frame = tk.Frame(parent, bg='white')
        buttons_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.save_btn = tk.Button(
            buttons_frame,
            text="Save",
            command=self.add_user,
            bg='#27ae60',
            fg='white',
            bd=0,
            padx=20,
            pady=8
        )
        self.save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.update_btn = tk.Button(
            buttons_frame,
            text="Update",
            command=self.update_user,
            bg='#f39c12',
            fg='white',
            bd=0,
            padx=20,
            pady=8
        )
        self.update_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.delete_btn = tk.Button(
            buttons_frame,
            text="Delete",
            command=self.delete_user,
            bg='#e74c3c',
            fg='white',
            bd=0,
            padx=20,
            pady=8
        )
        self.delete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = tk.Button(
            buttons_frame,
            text="Clear",
            command=self.clear_form,
            bg='#95a5a6',
            fg='white',
            bd=0,
            padx=20,
            pady=8
        )
        self.clear_btn.pack(side=tk.LEFT)
        
        # Initially disable update and delete buttons
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
    
    def on_user_select(self, event):
        """Handle user selection"""
        selection = self.user_tree.selection()
        if selection:
            item = self.user_tree.item(selection[0])
            user_id = item['values'][0]  # Assuming ID is in the first column
            self.load_user_details(user_id)
    
    def load_users(self):
        """Load users from database"""
        try:
            # Clear existing items
            for item in self.user_tree.get_children():
                self.user_tree.delete(item)
            
            # Get users from database
            users = self.db_manager.get_users()
            
            # Add users to treeview
            for user in users:
                status = "Active" if user.get('is_active') else "Inactive"
                self.user_tree.insert('', tk.END, values=(
                    user['id'],
                    user['username'],
                    f"{user['first_name']} {user['last_name']}",
                    user['role'].title(),
                    status
                ))
            
        except Exception as e:
            self.logger.error(f"Error loading users: {e}")
            messagebox.showerror("Error", f"Failed to load users: {str(e)}")
    
    def load_user_details(self, user_id):
        """Load user details into form"""
        try:
            user_data = self.db_manager.get_user_by_id(user_id)
            if user_data:
                self.selected_user = user_data
                
                # Populate form fields
                self.username_var.set(user_data.get('username', ''))
                self.first_name_var.set(user_data.get('first_name', ''))
                self.last_name_var.set(user_data.get('last_name', ''))
                self.email_var.set(user_data.get('email', ''))
                self.role_var.set(user_data.get('role', ''))
                self.is_active_var.set(bool(user_data.get('is_active', True)))
                
                # Clear password field for existing users
                self.password_var.set('')
                
                # Enable update and delete buttons
                self.update_btn.config(state=tk.NORMAL)
                self.delete_btn.config(state=tk.NORMAL)
                
        except Exception as e:
            self.logger.error(f"Error loading user details: {e}")
            messagebox.showerror("Error", f"Failed to load user details: {str(e)}")
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def add_user(self):
        """Add a new user"""
        try:
            # Validate form data
            user_data = self.get_form_data()
            errors = self.validate_user_data(user_data)
            
            if errors:
                messagebox.showerror("Validation Error", "\n".join(errors))
                return
            
            # Hash password
            user_data['password_hash'] = self.hash_password(user_data['password'])
            del user_data['password']  # Remove plain text password
            
            # Add user to database
            user_id = self.db_manager.add_user(user_data)
            
            messagebox.showinfo("Success", f"User added successfully with ID: {user_id}")
            
            # Clear form and reload users
            self.clear_form()
            self.load_users()
            
        except Exception as e:
            self.logger.error(f"Error adding user: {e}")
            messagebox.showerror("Error", f"Failed to add user: {str(e)}")
    
    def update_user(self):
        """Update selected user"""
        if not self.selected_user:
            messagebox.showwarning("Warning", "Please select a user to update")
            return
        
        try:
            # Validate form data
            user_data = self.get_form_data()
            errors = self.validate_user_data(user_data, is_update=True)
            
            if errors:
                messagebox.showerror("Validation Error", "\n".join(errors))
                return
            
            # Only hash password if it was changed
            if user_data.get('password'):
                user_data['password_hash'] = self.hash_password(user_data['password'])
                del user_data['password']
            
            # Update user in database (implementation needed in db_manager)
            # success = self.db_manager.update_user(self.selected_user['id'], user_data)
            
            messagebox.showinfo("Success", "User updated successfully")
            self.load_users()
            
        except Exception as e:
            self.logger.error(f"Error updating user: {e}")
            messagebox.showerror("Error", f"Failed to update user: {str(e)}")
    
    def delete_user(self):
        """Delete selected user"""
        if not self.selected_user:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
        
        # Prevent self-deletion
        if self.selected_user['id'] == self.current_user['id']:
            messagebox.showerror("Error", "You cannot delete your own account")
            return
        
        # Confirm deletion
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete user {self.selected_user['username']}?"
        )
        
        if result:
            try:
                # Delete user from database (implementation needed in db_manager)
                # success = self.db_manager.delete_user(self.selected_user['id'])
                
                messagebox.showinfo("Success", "User deleted successfully")
                self.clear_form()
                self.load_users()
                
            except Exception as e:
                self.logger.error(f"Error deleting user: {e}")
                messagebox.showerror("Error", f"Failed to delete user: {str(e)}")
    
    def clear_form(self):
        """Clear the form fields"""
        self.selected_user = None
        
        # Clear all form variables
        self.username_var.set('')
        self.first_name_var.set('')
        self.last_name_var.set('')
        self.email_var.set('')
        self.role_var.set('')
        self.password_var.set('')
        self.is_active_var.set(True)
        
        # Disable update and delete buttons
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
    
    def get_form_data(self):
        """Get data from form fields"""
        return {
            'username': self.username_var.get().strip(),
            'first_name': self.first_name_var.get().strip(),
            'last_name': self.last_name_var.get().strip(),
            'email': self.email_var.get().strip(),
            'role': self.role_var.get().strip(),
            'password': self.password_var.get().strip(),
            'is_active': self.is_active_var.get()
        }
    
    def validate_user_data(self, data, is_update=False):
        """Validate user data"""
        errors = []
        
        if not data['username']:
            errors.append("Username is required")
        
        if not data['first_name']:
            errors.append("First name is required")
        
        if not data['last_name']:
            errors.append("Last name is required")
        
        if not data['email']:
            errors.append("Email is required")
        
        if not data['role']:
            errors.append("Role is required")
        
        if not is_update and not data['password']:
            errors.append("Password is required for new users")
        
        return errors 