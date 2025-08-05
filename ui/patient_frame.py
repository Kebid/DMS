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
    
    def __init__(self, parent, db_manager, current_user=None):
        super().__init__(parent, bg='white')
        self.db_manager = db_manager
        self.current_user = current_user
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
        
        # Only show Add Patient button for receptionist and admin, not for doctors
        if not self.current_user or self.current_user.get('role') != 'doctor':
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
        
        # Age
        tk.Label(parent, text="Age:", bg='white').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.age_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.age_var, width=30).grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Treatment
        tk.Label(parent, text="Treatment:", bg='white').grid(row=3, column=0, sticky=tk.W, pady=5)
        self.treatment_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.treatment_var, width=30).grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Date of Birth
        tk.Label(parent, text="Date of Birth:", bg='white').grid(row=4, column=0, sticky=tk.W, pady=5)
        self.dob_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.dob_var, width=30).grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Phone
        tk.Label(parent, text="Phone:", bg='white').grid(row=5, column=0, sticky=tk.W, pady=5)
        self.phone_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.phone_var, width=30).grid(row=5, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Email
        tk.Label(parent, text="Email:", bg='white').grid(row=6, column=0, sticky=tk.W, pady=5)
        self.email_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.email_var, width=30).grid(row=6, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Address
        tk.Label(parent, text="Address:", bg='white').grid(row=7, column=0, sticky=tk.W, pady=5)
        self.address_text = tk.Text(parent, height=3, width=30)
        self.address_text.grid(row=7, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Emergency Contact
        tk.Label(parent, text="Emergency Contact:", bg='white').grid(row=8, column=0, sticky=tk.W, pady=5)
        self.emergency_contact_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.emergency_contact_var, width=30).grid(row=8, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Medical History (read-only for receptionist)
        tk.Label(parent, text="Medical History:", bg='white').grid(row=9, column=0, sticky=tk.W, pady=5)
        self.medical_history_text = tk.Text(parent, height=8, width=40, font=('Consolas', 9))
        self.medical_history_text.grid(row=9, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Add scrollbar for medical history
        medical_history_scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.medical_history_text.yview)
        self.medical_history_text.configure(yscrollcommand=medical_history_scrollbar.set)
        medical_history_scrollbar.grid(row=9, column=2, sticky=tk.NS, pady=5)
        
        self.apply_role_restrictions()
    
    def apply_role_restrictions(self):
        """Apply role-based restrictions to the UI"""
        if self.current_user and self.current_user.get('role') == 'receptionist':
            # Receptionist can only view medical history, not edit
            self.medical_history_text.config(state=tk.DISABLED)
        elif self.current_user and self.current_user.get('role') == 'doctor':
            # Doctor can edit medical history but cannot add new patients or edit patient info
            self.medical_history_text.config(state=tk.NORMAL)
            # Hide the Save, Clear, Update, and Delete buttons for doctors (they can't modify patients)
            if hasattr(self, 'save_btn'):
                self.save_btn.pack_forget()
            if hasattr(self, 'clear_btn'):
                self.clear_btn.pack_forget()
            if hasattr(self, 'update_btn'):
                self.update_btn.pack_forget()
            if hasattr(self, 'delete_btn'):
                self.delete_btn.pack_forget()
            # Disable form fields for doctors (read-only patient info)
            self.disable_form_fields()
        else:
            # Admin can edit medical history and add patients
            self.medical_history_text.config(state=tk.NORMAL)
    
    def disable_form_fields(self):
        """Disable form fields for read-only access (doctors)"""
        try:
            # Disable all entry fields
            if hasattr(self, 'first_name_entry'):
                self.first_name_entry.config(state=tk.DISABLED)
            if hasattr(self, 'last_name_entry'):
                self.last_name_entry.config(state=tk.DISABLED)
            if hasattr(self, 'age_entry'):
                self.age_entry.config(state=tk.DISABLED)
            if hasattr(self, 'treatment_entry'):
                self.treatment_entry.config(state=tk.DISABLED)
            if hasattr(self, 'dob_entry'):
                self.dob_entry.config(state=tk.DISABLED)
            if hasattr(self, 'phone_entry'):
                self.phone_entry.config(state=tk.DISABLED)
            if hasattr(self, 'email_entry'):
                self.email_entry.config(state=tk.DISABLED)
            if hasattr(self, 'emergency_contact_entry'):
                self.emergency_contact_entry.config(state=tk.DISABLED)
            
            # Disable text fields
            if hasattr(self, 'address_text'):
                self.address_text.config(state=tk.DISABLED)
                
        except Exception as e:
            self.logger.error(f"Error disabling form fields: {e}")
    
    def enable_form_fields(self):
        """Enable form fields for editing (receptionist/admin)"""
        try:
            # Enable all entry fields
            if hasattr(self, 'first_name_entry'):
                self.first_name_entry.config(state=tk.NORMAL)
            if hasattr(self, 'last_name_entry'):
                self.last_name_entry.config(state=tk.NORMAL)
            if hasattr(self, 'age_entry'):
                self.age_entry.config(state=tk.NORMAL)
            if hasattr(self, 'treatment_entry'):
                self.treatment_entry.config(state=tk.NORMAL)
            if hasattr(self, 'dob_entry'):
                self.dob_entry.config(state=tk.NORMAL)
            if hasattr(self, 'phone_entry'):
                self.phone_entry.config(state=tk.NORMAL)
            if hasattr(self, 'email_entry'):
                self.email_entry.config(state=tk.NORMAL)
            if hasattr(self, 'emergency_contact_entry'):
                self.emergency_contact_entry.config(state=tk.NORMAL)
            
            # Enable text fields
            if hasattr(self, 'address_text'):
                self.address_text.config(state=tk.NORMAL)
                
        except Exception as e:
            self.logger.error(f"Error enabling form fields: {e}")
    
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
        
        # Add Medical History button for doctors
        if self.current_user and self.current_user.get('role') == 'doctor':
            self.medical_history_btn = tk.Button(
                buttons_frame,
                text="Manage Medical History",
                command=self.open_medical_history,
                bg='#9b59b6',
                fg='white',
                bd=0,
                padx=20,
                pady=8
            )
            self.medical_history_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Initially disable update and delete buttons
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
    
    def open_medical_history(self):
        """Open medical history management window for doctors"""
        if not self.selected_patient:
            messagebox.showwarning("Warning", "Please select a patient first")
            return
        
        try:
            # Create a new window for medical history management
            history_window = tk.Toplevel(self)
            history_window.title(f"Medical History - {self.selected_patient['first_name']} {self.selected_patient['last_name']}")
            history_window.geometry("1000x600")
            history_window.configure(bg='white')
            
            # Create medical history frame
            from .medical_history_frame import MedicalHistoryFrame
            history_frame = MedicalHistoryFrame(
                history_window, 
                self.db_manager, 
                self.current_user, 
                self.selected_patient['id']
            )
            history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
        except Exception as e:
            self.logger.error(f"Error opening medical history: {e}")
            messagebox.showerror("Error", f"Failed to open medical history: {str(e)}")
    
    def load_doctors(self):
        """Load doctors for the dropdown"""
        try:
            doctors = self.db_manager.get_dentists()
            if doctors:
                # Since there's only one doctor, auto-assign it
                doctor = doctors[0]
                doctor_display = f"Dr. {doctor['username'].title()}"
                doctor_options = [doctor_display]
                self.doctor_combobox['values'] = doctor_options
                
                # Auto-assign doctor for receptionists
                if self.current_user and self.current_user.get('role') == 'receptionist':
                    self.assigned_doctor_var.set(doctor_display)
                else:
                    self.assigned_doctor_var.set(doctor_display)
            else:
                self.doctor_combobox['values'] = ["No doctors available"]
                self.assigned_doctor_var.set("No doctors available")
        except Exception as e:
            self.logger.error(f"Error loading doctors: {e}")
            messagebox.showerror("Error", f"Failed to load doctors: {str(e)}")
    
    def on_search_change(self, *args):
        """Handle search input changes"""
        self.load_patients()
    
    def on_patient_select(self, event):
        """Handle patient selection"""
        selection = self.patient_tree.selection()
        if selection:
            item = self.patient_tree.item(selection[0])
            patient_id = item['tags'][0]  # Get ID from tags
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
            if self.current_user and self.current_user.get('role') == 'doctor':
                # For doctors, only show their assigned patients
                patients = self.db_manager.get_patients(
                    search_term=search_term if search_term else None,
                    assigned_doctor=self.current_user.get('username')
                )
            else:
                # For other roles, show all patients
                patients = self.db_manager.get_patients(search_term=search_term if search_term else None)
            
            # Add patients to treeview
            for patient in patients:
                self.patient_tree.insert('', tk.END, values=(
                    f"{patient['first_name']} {patient['last_name']}",
                    patient.get('phone', ''),
                    patient.get('email', '')
                ), tags=(patient['id'],))
            
            # Show message if no patients found for doctor
            if self.current_user and self.current_user.get('role') == 'doctor' and not patients:
                messagebox.showinfo("No Patients", "No patients have been assigned to you yet.")
            
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
                self.age_var.set(str(patient_data.get('age', '')) if patient_data.get('age') else '')
                self.treatment_var.set(patient_data.get('treatment', ''))
                self.dob_var.set(patient_data.get('date_of_birth', ''))
                self.phone_var.set(patient_data.get('phone', ''))
                self.email_var.set(patient_data.get('email', ''))
                self.emergency_contact_var.set(patient_data.get('emergency_contact', ''))
                
                # Clear and set text fields
                self.address_text.delete(1.0, tk.END)
                self.address_text.insert(1.0, patient_data.get('address', ''))
                
                # Load medical history from separate table
                self.load_medical_history(patient_id)
                
                # Enable update and delete buttons
                self.update_btn.config(state=tk.NORMAL)
                self.delete_btn.config(state=tk.NORMAL)
                
                # Enable medical history button for doctors
                if self.current_user and self.current_user.get('role') == 'doctor':
                    if hasattr(self, 'medical_history_btn'):
                        self.medical_history_btn.config(state=tk.NORMAL)
                
        except Exception as e:
            self.logger.error(f"Error loading patient details: {e}")
            messagebox.showerror("Error", f"Failed to load patient details: {str(e)}")
    
    def load_medical_history(self, patient_id):
        """Load medical history from the medical_history table"""
        try:
            # Clear existing medical history
            self.medical_history_text.delete(1.0, tk.END)
            
            # Get medical history from database
            medical_history = self.db_manager.get_medical_history(patient_id)
            
            # Debug logging
            self.logger.info(f"Loading medical history for patient {patient_id}")
            self.logger.info(f"Found {len(medical_history)} medical history entries")
            
            if medical_history:
                # Format and display medical history with better UI
                history_text = "📋 MEDICAL HISTORY SUMMARY\n"
                history_text += "=" * 50 + "\n\n"
                
                for i, entry in enumerate(medical_history, 1):
                    date = entry.get('date', 'Unknown Date')
                    note = entry.get('note', '')
                    
                    # Parse the note to extract treatment and cost
                    treatment = "General"
                    cost = "$0"
                    notes = ""
                    
                    if "Treatment:" in note and "Cost:" in note:
                        parts = note.split("Cost:")
                        if len(parts) == 2:
                            treatment_part = parts[0].replace("Treatment:", "").strip()
                            cost_part = parts[1].strip()
                            if "Notes:" in cost_part:
                                cost_notes = cost_part.split("Notes:")
                                cost = cost_notes[0].strip()
                                notes = cost_notes[1].strip() if len(cost_notes) > 1 else ""
                            else:
                                cost = cost_part
                            treatment = treatment_part
                    
                    self.logger.info(f"Medical history entry: {date} - {note}")
                    
                    # Format each entry nicely
                    history_text += f"📅 Entry #{i} - {date}\n"
                    history_text += f"🦷 Treatment: {treatment}\n"
                    history_text += f"💰 Cost: {cost}\n"
                    if notes:
                        history_text += f"📝 Notes: {notes}\n"
                    history_text += "-" * 40 + "\n\n"
                
                # Temporarily enable text widget to insert content
                current_state = self.medical_history_text.cget('state')
                self.medical_history_text.config(state=tk.NORMAL)
                self.medical_history_text.insert(1.0, history_text)
                # Restore original state
                self.medical_history_text.config(state=current_state)
            else:
                # Temporarily enable text widget to insert content
                current_state = self.medical_history_text.cget('state')
                self.medical_history_text.config(state=tk.NORMAL)
                self.medical_history_text.insert(1.0, "📋 MEDICAL HISTORY\n" + "=" * 30 + "\n\nNo medical history available.")
                # Restore original state
                self.medical_history_text.config(state=current_state)
                
        except Exception as e:
            self.logger.error(f"Error loading medical history: {e}")
            # Temporarily enable text widget to insert content
            current_state = self.medical_history_text.cget('state')
            self.medical_history_text.config(state=tk.NORMAL)
            self.medical_history_text.insert(1.0, "❌ Error loading medical history.")
            # Restore original state
            self.medical_history_text.config(state=current_state)
    
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
                # Delete patient from database
                success = self.db_manager.delete_patient(self.selected_patient['id'])
                
                if success:
                    messagebox.showinfo("Success", "Patient deleted successfully")
                    self.clear_form()
                    self.load_patients()
                else:
                    messagebox.showerror("Error", "Failed to delete patient")
                
            except Exception as e:
                self.logger.error(f"Error deleting patient: {e}")
                messagebox.showerror("Error", f"Failed to delete patient: {str(e)}")
    
    def clear_form(self):
        """Clear the form fields"""
        self.selected_patient = None
        
        # Clear all form variables
        self.first_name_var.set('')
        self.last_name_var.set('')
        self.age_var.set('')
        self.treatment_var.set('')
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
        
        # Disable medical history button for doctors
        if self.current_user and self.current_user.get('role') == 'doctor':
            if hasattr(self, 'medical_history_btn'):
                self.medical_history_btn.config(state=tk.DISABLED)
    
    def get_form_data(self):
        """Get data from form fields"""
        # Auto-assign doctor since there's only one doctor
        assigned_doctor = None
        try:
            doctors = self.db_manager.get_dentists()
            if doctors:
                assigned_doctor = doctors[0]['username']
        except Exception as e:
            self.logger.error(f"Error auto-assigning doctor: {e}")
        
        return {
            'first_name': self.first_name_var.get().strip(),
            'last_name': self.last_name_var.get().strip(),
            'age': int(self.age_var.get().strip()) if self.age_var.get().strip() else None,
            'treatment': self.treatment_var.get().strip(),
            'date_of_birth': self.dob_var.get().strip(),
            'phone': self.phone_var.get().strip(),
            'email': self.email_var.get().strip(),
            'address': self.address_text.get(1.0, tk.END).strip(),
            'emergency_contact': self.emergency_contact_var.get().strip(),
            'medical_history': self.medical_history_text.get(1.0, tk.END).strip(),
            'assigned_doctor': assigned_doctor
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