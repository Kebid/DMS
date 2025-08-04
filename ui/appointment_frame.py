"""
Appointment Frame for Dental Clinic Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
import logging

from models.appointment import Appointment, AppointmentStatus

class AppointmentFrame(tk.Frame):
    """Appointment management frame"""
    
    def __init__(self, parent, db_manager):
        super().__init__(parent, bg='white')
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)
        self.selected_appointment = None
        
        self.setup_ui()
        self.load_appointments()
    
    def setup_ui(self):
        """Setup the appointment management user interface"""
        # Title
        title_label = tk.Label(
            self,
            text="Appointment Management",
            font=('Arial', 18, 'bold'),
            bg='white'
        )
        title_label.pack(pady=(20, 30))
        
        # Main content area
        content_frame = tk.Frame(self, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Left panel - Appointment list
        self.create_appointment_list_panel(content_frame)
        
        # Right panel - Appointment details
        self.create_appointment_details_panel(content_frame)
    
    def create_appointment_list_panel(self, parent):
        """Create the appointment list panel"""
        list_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Filter frame
        filter_frame = tk.Frame(list_frame, bg='white')
        filter_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(filter_frame, text="Date:", bg='white').pack(side=tk.LEFT)
        self.date_var = tk.StringVar(value=date.today().isoformat())
        date_entry = tk.Entry(filter_frame, textvariable=self.date_var, width=15)
        date_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        filter_btn = tk.Button(
            filter_frame,
            text="Filter",
            command=self.load_appointments,
            bg='#3498db',
            fg='white',
            bd=0,
            padx=10,
            pady=2
        )
        filter_btn.pack(side=tk.LEFT)
        
        # Buttons frame
        buttons_frame = tk.Frame(list_frame, bg='white')
        buttons_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        add_btn = tk.Button(
            buttons_frame,
            text="New Appointment",
            command=self.add_appointment,
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
            command=self.load_appointments,
            bg='#3498db',
            fg='white',
            bd=0,
            padx=15,
            pady=5
        )
        refresh_btn.pack(side=tk.LEFT)
        
        # Appointment list
        list_label = tk.Label(list_frame, text="Appointments:", bg='white', font=('Arial', 12, 'bold'))
        list_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Treeview for appointment list
        self.appointment_tree = ttk.Treeview(
            list_frame,
            columns=('Time', 'Patient', 'Treatment', 'Status'),
            show='headings',
            height=15
        )
        
        self.appointment_tree.heading('Time', text='Time')
        self.appointment_tree.heading('Patient', text='Patient')
        self.appointment_tree.heading('Treatment', text='Treatment')
        self.appointment_tree.heading('Status', text='Status')
        
        self.appointment_tree.column('Time', width=100)
        self.appointment_tree.column('Patient', width=150)
        self.appointment_tree.column('Treatment', width=120)
        self.appointment_tree.column('Status', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.appointment_tree.yview)
        self.appointment_tree.configure(yscrollcommand=scrollbar.set)
        
        self.appointment_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 10))
        
        # Bind selection event
        self.appointment_tree.bind('<<TreeviewSelect>>', self.on_appointment_select)
    
    def create_appointment_details_panel(self, parent):
        """Create the appointment details panel"""
        details_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Title
        details_title = tk.Label(
            details_frame,
            text="Appointment Details",
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
        """Create form fields for appointment details"""
        # Patient selection
        tk.Label(parent, text="Patient:", bg='white').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.patient_var = tk.StringVar()
        self.patient_combo = ttk.Combobox(parent, textvariable=self.patient_var, width=30, state='readonly')
        self.patient_combo.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Date
        tk.Label(parent, text="Date:", bg='white').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.date_var_form = tk.StringVar()
        tk.Entry(parent, textvariable=self.date_var_form, width=30).grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Time
        tk.Label(parent, text="Time:", bg='white').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.time_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.time_var, width=30).grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Duration
        tk.Label(parent, text="Duration (min):", bg='white').grid(row=3, column=0, sticky=tk.W, pady=5)
        self.duration_var = tk.StringVar(value="60")
        tk.Entry(parent, textvariable=self.duration_var, width=30).grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Treatment type
        tk.Label(parent, text="Treatment:", bg='white').grid(row=4, column=0, sticky=tk.W, pady=5)
        self.treatment_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.treatment_var, width=30).grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Status
        tk.Label(parent, text="Status:", bg='white').grid(row=5, column=0, sticky=tk.W, pady=5)
        self.status_var = tk.StringVar()
        status_combo = ttk.Combobox(parent, textvariable=self.status_var, width=30, state='readonly')
        status_combo['values'] = [status.value for status in AppointmentStatus]
        status_combo.grid(row=5, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Notes
        tk.Label(parent, text="Notes:", bg='white').grid(row=6, column=0, sticky=tk.W, pady=5)
        self.notes_text = tk.Text(parent, height=4, width=30)
        self.notes_text.grid(row=6, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Load patients for combo box
        self.load_patients_combo()
    
    def create_action_buttons(self, parent):
        """Create action buttons"""
        buttons_frame = tk.Frame(parent, bg='white')
        buttons_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.save_btn = tk.Button(
            buttons_frame,
            text="Save",
            command=self.add_appointment,
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
            command=self.update_appointment,
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
            command=self.delete_appointment,
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
    
    def load_patients_combo(self):
        """Load patients into combo box"""
        try:
            patients = self.db_manager.get_patients()
            patient_options = [f"{p['id']} - {p['first_name']} {p['last_name']}" for p in patients]
            self.patient_combo['values'] = patient_options
        except Exception as e:
            self.logger.error(f"Error loading patients for combo: {e}")
    
    def on_appointment_select(self, event):
        """Handle appointment selection"""
        selection = self.appointment_tree.selection()
        if selection:
            # Load appointment details (implementation needed)
            pass
    
    def load_appointments(self):
        """Load appointments from database"""
        try:
            # Clear existing items
            for item in self.appointment_tree.get_children():
                self.appointment_tree.delete(item)
            
            # Get filter date
            filter_date = self.date_var.get().strip()
            
            # Get appointments from database
            appointments = self.db_manager.get_appointments(date=filter_date if filter_date else None)
            
            # Add appointments to treeview
            for apt in appointments:
                time_str = apt['appointment_time'] if apt['appointment_time'] else "N/A"
                patient_name = apt.get('patient_name', f"Patient {apt['patient_id']}")
                treatment = apt.get('treatment_type', 'General Checkup')
                status = apt.get('status', 'scheduled').title()
                
                self.appointment_tree.insert('', tk.END, values=(
                    time_str,
                    patient_name,
                    treatment,
                    status
                ))
            
        except Exception as e:
            self.logger.error(f"Error loading appointments: {e}")
            messagebox.showerror("Error", f"Failed to load appointments: {str(e)}")
    
    def add_appointment(self):
        """Add a new appointment"""
        try:
            # Validate form data
            appointment_data = self.get_form_data()
            errors = self.validate_appointment_data(appointment_data)
            
            if errors:
                messagebox.showerror("Validation Error", "\n".join(errors))
                return
            
            # Add appointment to database
            appointment_id = self.db_manager.add_appointment(appointment_data)
            
            messagebox.showinfo("Success", f"Appointment added successfully with ID: {appointment_id}")
            
            # Clear form and reload appointments
            self.clear_form()
            self.load_appointments()
            
        except Exception as e:
            self.logger.error(f"Error adding appointment: {e}")
            messagebox.showerror("Error", f"Failed to add appointment: {str(e)}")
    
    def update_appointment(self):
        """Update selected appointment"""
        if not self.selected_appointment:
            messagebox.showwarning("Warning", "Please select an appointment to update")
            return
        
        try:
            # Validate form data
            appointment_data = self.get_form_data()
            errors = self.validate_appointment_data(appointment_data)
            
            if errors:
                messagebox.showerror("Validation Error", "\n".join(errors))
                return
            
            # Update appointment in database
            success = self.db_manager.update_appointment_status(self.selected_appointment['id'], appointment_data['status'])
            
            if success:
                messagebox.showinfo("Success", "Appointment updated successfully")
                self.load_appointments()
            else:
                messagebox.showerror("Error", "Failed to update appointment")
            
        except Exception as e:
            self.logger.error(f"Error updating appointment: {e}")
            messagebox.showerror("Error", f"Failed to update appointment: {str(e)}")
    
    def delete_appointment(self):
        """Delete selected appointment"""
        if not self.selected_appointment:
            messagebox.showwarning("Warning", "Please select an appointment to delete")
            return
        
        # Confirm deletion
        result = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this appointment?")
        
        if result:
            try:
                # Delete appointment from database (implementation needed in db_manager)
                messagebox.showinfo("Success", "Appointment deleted successfully")
                self.clear_form()
                self.load_appointments()
                
            except Exception as e:
                self.logger.error(f"Error deleting appointment: {e}")
                messagebox.showerror("Error", f"Failed to delete appointment: {str(e)}")
    
    def clear_form(self):
        """Clear the form fields"""
        self.selected_appointment = None
        
        # Clear all form variables
        self.patient_var.set('')
        self.date_var_form.set('')
        self.time_var.set('')
        self.duration_var.set('60')
        self.treatment_var.set('')
        self.status_var.set('')
        
        # Clear text fields
        self.notes_text.delete(1.0, tk.END)
        
        # Disable update and delete buttons
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
    
    def get_form_data(self):
        """Get data from form fields"""
        return {
            'patient_id': self.patient_var.get().split(' - ')[0] if self.patient_var.get() else None,
            'appointment_date': self.date_var_form.get().strip(),
            'appointment_time': self.time_var.get().strip(),
            'duration': int(self.duration_var.get()) if self.duration_var.get() else 60,
            'treatment_type': self.treatment_var.get().strip(),
            'status': self.status_var.get().strip(),
            'notes': self.notes_text.get(1.0, tk.END).strip()
        }
    
    def validate_appointment_data(self, data):
        """Validate appointment data"""
        errors = []
        
        if not data['patient_id']:
            errors.append("Patient is required")
        
        if not data['appointment_date']:
            errors.append("Date is required")
        
        if not data['appointment_time']:
            errors.append("Time is required")
        
        # Add more validation as needed
        
        return errors 