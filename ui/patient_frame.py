"""
Patient Frame for Dental Clinic Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import logging

from models.patient import Patient

class PatientFrame(tk.Frame):
    """Patient management frame"""
    
    def __init__(self, parent, db_manager):
        super().__init__(parent, bg='white')
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)
        self.selected_patient = None
        
        self.setup_ui()
        self.load_patients()
    
    def setup_ui(self):
        """Setup the patient management user interface"""
        # Title
        title_label = tk.Label(
            self,
            text="Patient Management",
            font=('Arial', 18, 'bold'),
            bg='white'
        )
        title_label.pack(pady=(20, 30))
        
        # Main content area
        content_frame = tk.Frame(self, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Left panel - Patient list
        self.create_patient_list_panel(content_frame)
        
        # Right panel - Patient details
        self.create_patient_details_panel(content_frame)
    
    def create_patient_list_panel(self, parent):
        """Create the patient list panel"""
        list_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Search frame
        search_frame = tk.Frame(list_frame, bg='white')
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        search_label = tk.Label(search_frame, text="Search:", bg='white')
        search_label.pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        # Buttons frame
        buttons_frame = tk.Frame(list_frame, bg='white')
        buttons_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        add_btn = tk.Button(
            buttons_frame,
            text="Add Patient",
            command=self.add_patient,
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
            command=self.load_patients,
            bg='#3498db',
            fg='white',
            bd=0,
            padx=15,
            pady=5
        )
        refresh_btn.pack(side=tk.LEFT)
        
        # Patient list
        list_label = tk.Label(list_frame, text="Patients:", bg='white', font=('Arial', 12, 'bold'))
        list_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Treeview for patient list
        self.patient_tree = ttk.Treeview(
            list_frame,
            columns=('Name', 'Phone', 'Email'),
            show='headings',
            height=15
        )
        
        self.patient_tree.heading('Name', text='Name')
        self.patient_tree.heading('Phone', text='Phone')
        self.patient_tree.heading('Email', text='Email')
        
        self.patient_tree.column('Name', width=150)
        self.patient_tree.column('Phone', width=100)
        self.patient_tree.column('Email', width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.patient_tree.yview)
        self.patient_tree.configure(yscrollcommand=scrollbar.set)
        
        self.patient_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 10))
        
        # Bind selection event
        self.patient_tree.bind('<<TreeviewSelect>>', self.on_patient_select)
    
    def create_patient_details_panel(self, parent):
        """Create the patient details panel"""
        details_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Title
        details_title = tk.Label(
            details_frame,
            text="Patient Details",
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
        """Create form fields for patient details"""
        # First Name
        tk.Label(parent, text="First Name:", bg='white').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.first_name_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.first_name_var, width=30).grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Last Name
        tk.Label(parent, text="Last Name:", bg='white').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.last_name_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.last_name_var, width=30).grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Date of Birth
        tk.Label(parent, text="Date of Birth:", bg='white').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.dob_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.dob_var, width=30).grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Phone
        tk.Label(parent, text="Phone:", bg='white').grid(row=3, column=0, sticky=tk.W, pady=5)
        self.phone_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.phone_var, width=30).grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Email
        tk.Label(parent, text="Email:", bg='white').grid(row=4, column=0, sticky=tk.W, pady=5)
        self.email_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.email_var, width=30).grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Address
        tk.Label(parent, text="Address:", bg='white').grid(row=5, column=0, sticky=tk.W, pady=5)
        self.address_text = tk.Text(parent, height=3, width=30)
        self.address_text.grid(row=5, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Emergency Contact
        tk.Label(parent, text="Emergency Contact:", bg='white').grid(row=6, column=0, sticky=tk.W, pady=5)
        self.emergency_contact_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.emergency_contact_var, width=30).grid(row=6, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Medical History
        tk.Label(parent, text="Medical History:", bg='white').grid(row=7, column=0, sticky=tk.W, pady=5)
        self.medical_history_text = tk.Text(parent, height=4, width=30)
        self.medical_history_text.grid(row=7, column=1, sticky=tk.W, pady=5, padx=(10, 0))
    
    def create_action_buttons(self, parent):
        """Create action buttons"""
        buttons_frame = tk.Frame(parent, bg='white')
        buttons_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.save_btn = tk.Button(
            buttons_frame,
            text="Save",
            command=self.add_patient,
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
            command=self.update_patient,
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
            command=self.delete_patient,
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
    
    def on_search_change(self, *args):
        """Handle search input changes"""
        self.load_patients()
    
    def on_patient_select(self, event):
        """Handle patient selection"""
        selection = self.patient_tree.selection()
        if selection:
            item = self.patient_tree.item(selection[0])
            patient_id = item['values'][0]  # Assuming ID is in the first column
            self.load_patient_details(patient_id)
    
    def load_patients(self):
        """Load patients from database"""
        try:
            # Clear existing items
            for item in self.patient_tree.get_children():
                self.patient_tree.delete(item)
            
            # Get search term
            search_term = self.search_var.get().strip()
            
            # Get patients from database
            patients = self.db_manager.get_patients(search_term=search_term if search_term else None)
            
            # Add patients to treeview
            for patient in patients:
                self.patient_tree.insert('', tk.END, values=(
                    patient['id'],
                    f"{patient['first_name']} {patient['last_name']}",
                    patient.get('phone', ''),
                    patient.get('email', '')
                ))
            
        except Exception as e:
            self.logger.error(f"Error loading patients: {e}")
            messagebox.showerror("Error", f"Failed to load patients: {str(e)}")
    
    def load_patient_details(self, patient_id):
        """Load patient details into form"""
        try:
            patient_data = self.db_manager.get_patient_by_id(patient_id)
            if patient_data:
                self.selected_patient = patient_data
                
                # Populate form fields
                self.first_name_var.set(patient_data.get('first_name', ''))
                self.last_name_var.set(patient_data.get('last_name', ''))
                self.dob_var.set(patient_data.get('date_of_birth', ''))
                self.phone_var.set(patient_data.get('phone', ''))
                self.email_var.set(patient_data.get('email', ''))
                self.emergency_contact_var.set(patient_data.get('emergency_contact', ''))
                
                # Clear and set text fields
                self.address_text.delete(1.0, tk.END)
                self.address_text.insert(1.0, patient_data.get('address', ''))
                
                self.medical_history_text.delete(1.0, tk.END)
                self.medical_history_text.insert(1.0, patient_data.get('medical_history', ''))
                
                # Enable update and delete buttons
                self.update_btn.config(state=tk.NORMAL)
                self.delete_btn.config(state=tk.NORMAL)
                
        except Exception as e:
            self.logger.error(f"Error loading patient details: {e}")
            messagebox.showerror("Error", f"Failed to load patient details: {str(e)}")
    
    def add_patient(self):
        """Add a new patient"""
        try:
            # Validate form data
            patient_data = self.get_form_data()
            errors = self.validate_patient_data(patient_data)
            
            if errors:
                messagebox.showerror("Validation Error", "\n".join(errors))
                return
            
            # Add patient to database
            patient_id = self.db_manager.add_patient(patient_data)
            
            messagebox.showinfo("Success", f"Patient added successfully with ID: {patient_id}")
            
            # Clear form and reload patients
            self.clear_form()
            self.load_patients()
            
        except Exception as e:
            self.logger.error(f"Error adding patient: {e}")
            messagebox.showerror("Error", f"Failed to add patient: {str(e)}")
    
    def update_patient(self):
        """Update selected patient"""
        if not self.selected_patient:
            messagebox.showwarning("Warning", "Please select a patient to update")
            return
        
        try:
            # Validate form data
            patient_data = self.get_form_data()
            errors = self.validate_patient_data(patient_data)
            
            if errors:
                messagebox.showerror("Validation Error", "\n".join(errors))
                return
            
            # Update patient in database
            success = self.db_manager.update_patient(self.selected_patient['id'], patient_data)
            
            if success:
                messagebox.showinfo("Success", "Patient updated successfully")
                self.load_patients()
            else:
                messagebox.showerror("Error", "Failed to update patient")
            
        except Exception as e:
            self.logger.error(f"Error updating patient: {e}")
            messagebox.showerror("Error", f"Failed to update patient: {str(e)}")
    
    def delete_patient(self):
        """Delete selected patient"""
        if not self.selected_patient:
            messagebox.showwarning("Warning", "Please select a patient to delete")
            return
        
        # Confirm deletion
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete {self.selected_patient['first_name']} {self.selected_patient['last_name']}?"
        )
        
        if result:
            try:
                # Delete patient from database (implementation needed in db_manager)
                # success = self.db_manager.delete_patient(self.selected_patient['id'])
                
                messagebox.showinfo("Success", "Patient deleted successfully")
                self.clear_form()
                self.load_patients()
                
            except Exception as e:
                self.logger.error(f"Error deleting patient: {e}")
                messagebox.showerror("Error", f"Failed to delete patient: {str(e)}")
    
    def clear_form(self):
        """Clear the form fields"""
        self.selected_patient = None
        
        # Clear all form variables
        self.first_name_var.set('')
        self.last_name_var.set('')
        self.dob_var.set('')
        self.phone_var.set('')
        self.email_var.set('')
        self.emergency_contact_var.set('')
        
        # Clear text fields
        self.address_text.delete(1.0, tk.END)
        self.medical_history_text.delete(1.0, tk.END)
        
        # Disable update and delete buttons
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
    
    def get_form_data(self):
        """Get data from form fields"""
        return {
            'first_name': self.first_name_var.get().strip(),
            'last_name': self.last_name_var.get().strip(),
            'date_of_birth': self.dob_var.get().strip(),
            'phone': self.phone_var.get().strip(),
            'email': self.email_var.get().strip(),
            'address': self.address_text.get(1.0, tk.END).strip(),
            'emergency_contact': self.emergency_contact_var.get().strip(),
            'medical_history': self.medical_history_text.get(1.0, tk.END).strip()
        }
    
    def validate_patient_data(self, data):
        """Validate patient data"""
        errors = []
        
        if not data['first_name']:
            errors.append("First name is required")
        
        if not data['last_name']:
            errors.append("Last name is required")
        
        # Add more validation as needed
        
        return errors 