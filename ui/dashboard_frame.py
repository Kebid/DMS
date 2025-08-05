"""
Dashboard Frame for Dental Clinic Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
import logging

class DashboardFrame(tk.Frame):
    """Dashboard frame showing role-specific overview information"""
    
    def __init__(self, parent, db_manager, current_user=None, main_window=None):
        super().__init__(parent, bg='white')
        self.db_manager = db_manager
        self.current_user = current_user
        self.main_window = main_window  # Reference to main window for navigation
        self.logger = logging.getLogger(__name__)
        
        self.setup_ui()
        self.load_dashboard_data()
    
    def setup_ui(self):
        """Setup the dashboard user interface"""
        # Welcome message based on role
        role = self.current_user.get('role', 'staff') if self.current_user else 'staff'
        welcome_text = f"Welcome, {role.title()}"
        
        welcome_label = tk.Label(
            self,
            text=welcome_text,
            font=('Arial', 20, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        welcome_label.pack(pady=(20, 10))
        
        # Subtitle
        subtitle_text = self.get_role_subtitle(role)
        subtitle_label = tk.Label(
            self,
            text=subtitle_text,
            font=('Arial', 12),
            fg='#7f8c8d',
            bg='white'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Create main content area
        content_frame = tk.Frame(self, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Create role-specific statistics cards
        self.create_role_statistics_cards(content_frame, role)
        
        # Create today's appointments section (for all roles)
        self.create_todays_appointments(content_frame)
        
        # Create role-specific quick actions
        self.create_role_quick_actions(content_frame, role)
    
    def get_role_subtitle(self, role):
        """Get role-specific subtitle"""
        subtitles = {
            'admin': 'System Administrator - Full Access',
            'receptionist': 'Patient Management & Scheduling',
            'doctor': 'Patient Care & Treatment',
            'dentist': 'Patient Care & Treatment',
            'hygienist': 'Dental Hygiene Services',
            'staff': 'General Staff Access'
        }
        return subtitles.get(role, 'General Access')
    
    def create_role_statistics_cards(self, parent, role):
        """Create role-specific statistics cards"""
        stats_frame = tk.Frame(parent, bg='white')
        stats_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Statistics cards
        self.stats_cards = {}
        
        if role == 'receptionist':
            stats_data = [
                ("Total Patients", "0", "#3498db"),
                ("Today's Appointments", "0", "#e74c3c"),
                ("Pending Appointments", "0", "#f39c12"),
                ("Outstanding Invoices", "0", "#9b59b6")
            ]
        elif role in ['dentist', 'doctor']:
            stats_data = [
                ("Today's Appointments", "0", "#e74c3c"),
                ("Patients Seen Today", "0", "#27ae60"),
                ("Pending Treatments", "0", "#f39c12"),
                ("Treatment Records", "0", "#3498db")
            ]
        else:  # admin or other roles
            stats_data = [
                ("Total Patients", "0", "#3498db"),
                ("Today's Appointments", "0", "#e74c3c"),
                ("Pending Appointments", "0", "#f39c12"),
                ("Total Treatments", "0", "#27ae60")
            ]
        
        for i, (title, value, color) in enumerate(stats_data):
            card_frame = tk.Frame(stats_frame, bg=color, relief=tk.RAISED, bd=2)
            card_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            # Value label
            value_label = tk.Label(
                card_frame,
                text=value,
                font=('Arial', 24, 'bold'),
                fg='white',
                bg=color
            )
            value_label.pack(pady=(15, 5))
            
            # Title label
            title_label = tk.Label(
                card_frame,
                text=title,
                font=('Arial', 10),
                fg='white',
                bg=color
            )
            title_label.pack(pady=(0, 15))
            
            self.stats_cards[title] = value_label
    
    def create_todays_appointments(self, parent):
        """Create today's appointments section"""
        appointments_frame = tk.Frame(parent, bg='white')
        appointments_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Section title
        section_title = tk.Label(
            appointments_frame,
            text="Today's Appointments",
            font=('Arial', 14, 'bold'),
            bg='white'
        )
        section_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Appointments list
        self.appointments_tree = ttk.Treeview(
            appointments_frame,
            columns=('Time', 'Patient', 'Treatment', 'Status'),
            show='headings',
            height=6
        )
        
        # Configure columns
        self.appointments_tree.heading('Time', text='Time')
        self.appointments_tree.heading('Patient', text='Patient')
        self.appointments_tree.heading('Treatment', text='Treatment')
        self.appointments_tree.heading('Status', text='Status')
        
        self.appointments_tree.column('Time', width=100)
        self.appointments_tree.column('Patient', width=200)
        self.appointments_tree.column('Treatment', width=150)
        self.appointments_tree.column('Status', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(appointments_frame, orient=tk.VERTICAL, command=self.appointments_tree.yview)
        self.appointments_tree.configure(yscrollcommand=scrollbar.set)
        
        self.appointments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_role_quick_actions(self, parent, role):
        """Create role-specific quick actions"""
        actions_frame = tk.Frame(parent, bg='white')
        actions_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Section title
        section_title = tk.Label(
            actions_frame,
            text="Quick Actions",
            font=('Arial', 14, 'bold'),
            bg='white'
        )
        section_title.pack(anchor=tk.W, pady=(0, 15))
        
        # Role-specific actions
        if role == 'receptionist':
            actions = [
                ("Quick Add Patient", self.quick_add_patient, "#27ae60"),
                ("Manage Patients", self.manage_patients, "#3498db"),
                ("Schedule Appointments", self.schedule_appointments, "#e74c3c"),
                ("Generate Invoices", self.generate_invoices, "#9b59b6"),
                ("View Calendar", self.view_calendar, "#f39c12")
            ]
        elif role in ['dentist', 'doctor']:
            actions = [
                ("View Today's Appointments", self.view_todays_appointments, "#e74c3c"),
                ("Manage Medical History", self.manage_medical_history, "#3498db"),
                ("Add Treatment Records", self.add_treatment_records, "#27ae60"),
                ("Patient Search", self.patient_search, "#f39c12")
            ]
        else:  # admin or other roles
            actions = [
                ("Manage Patients", self.manage_patients, "#3498db"),
                ("Schedule Appointments", self.schedule_appointments, "#e74c3c"),
                ("View Treatments", self.view_treatments, "#27ae60"),
                ("Generate Reports", self.generate_reports, "#9b59b6")
            ]
        
        # Create action buttons
        for i, (text, command, color) in enumerate(actions):
            btn = tk.Button(
                actions_frame,
                text=text,
                command=command,
                font=('Arial', 11, 'bold'),
                bg=color,
                fg='white',
                bd=0,
                padx=20,
                pady=12,
                cursor='hand2',
                width=20
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
            
            # Bind hover events
            btn.bind('<Enter>', lambda e, b=btn, c=color: self.on_button_hover(b, True, c))
            btn.bind('<Leave>', lambda e, b=btn, c=color: self.on_button_hover(b, False, c))
    
    def on_button_hover(self, button: tk.Button, entering: bool, original_color: str):
        """Handle button hover events"""
        if entering:
            # Darken the color slightly
            button.configure(bg=self.darken_color(original_color))
        else:
            button.configure(bg=original_color)
    
    def darken_color(self, color: str) -> str:
        """Darken a hex color for hover effect"""
        # Simple darkening - in a real app you'd use a proper color library
        return color  # For now, return same color
    
    def load_dashboard_data(self):
        """Load dashboard data from database"""
        try:
            # Load statistics
            self.load_statistics()
            
            # Load today's appointments
            self.load_todays_appointments()
            
        except Exception as e:
            self.logger.error(f"Error loading dashboard data: {e}")
    
    def load_statistics(self):
        """Load and display statistics"""
        try:
            role = self.current_user.get('role', 'staff') if self.current_user else 'staff'
            
            # Get total patients
            patients = self.db_manager.get_patients()
            if "Total Patients" in self.stats_cards:
                self.stats_cards["Total Patients"].configure(text=str(len(patients)))
            
            # Get today's appointments
            today = date.today().isoformat()
            today_appointments = self.db_manager.get_appointments(date=today)
            if "Today's Appointments" in self.stats_cards:
                self.stats_cards["Today's Appointments"].configure(text=str(len(today_appointments)))
            
            # Get pending appointments (scheduled status)
            all_appointments = self.db_manager.get_appointments()
            pending_count = sum(1 for apt in all_appointments if apt['status'] == 'scheduled')
            if "Pending Appointments" in self.stats_cards:
                self.stats_cards["Pending Appointments"].configure(text=str(pending_count))
            
            # Get total treatments
            treatments = self.db_manager.get_treatments()
            if "Total Treatments" in self.stats_cards:
                self.stats_cards["Total Treatments"].configure(text=str(len(treatments)))
            
            # Role-specific statistics
            if role == 'receptionist':
                # Outstanding invoices (placeholder)
                if "Outstanding Invoices" in self.stats_cards:
                    self.stats_cards["Outstanding Invoices"].configure(text="0")
            
            elif role == 'dentist':
                # Patients seen today (placeholder)
                if "Patients Seen Today" in self.stats_cards:
                    self.stats_cards["Patients Seen Today"].configure(text="0")
                
                # Pending treatments (placeholder)
                if "Pending Treatments" in self.stats_cards:
                    self.stats_cards["Pending Treatments"].configure(text="0")
                
                # Treatment records (placeholder)
                if "Treatment Records" in self.stats_cards:
                    self.stats_cards["Treatment Records"].configure(text="0")
            
        except Exception as e:
            self.logger.error(f"Error loading statistics: {e}")
    
    def load_todays_appointments(self):
        """Load and display today's appointments"""
        try:
            # Clear existing items
            for item in self.appointments_tree.get_children():
                self.appointments_tree.delete(item)
            
            # Get today's appointments
            today = date.today().isoformat()
            appointments = self.db_manager.get_appointments(date=today)
            
            # Add appointments to treeview
            for apt in appointments:
                time_str = apt['appointment_time'] if apt['appointment_time'] else "N/A"
                patient_name = apt.get('patient_name', f"Patient {apt['patient_id']}")
                treatment = apt.get('appointment_type', 'General Checkup')
                status = apt.get('status', 'scheduled').title()
                
                self.appointments_tree.insert('', tk.END, values=(
                    time_str,
                    patient_name,
                    treatment,
                    status
                ))
            
        except Exception as e:
            self.logger.error(f"Error loading today's appointments: {e}")
    
    # Receptionist Quick Actions
    def quick_add_patient(self):
        """Quick action: Open simplified patient addition dialog"""
        self.show_quick_patient_dialog()
    
    def manage_patients(self):
        """Quick action: Navigate to patient management"""
        if self.main_window:
            self.main_window.show_patients()
        else:
            messagebox.showinfo("Quick Action", "Navigate to Patient Management section")
    
    def schedule_appointments(self):
        """Quick action: Navigate to appointment management"""
        if self.main_window:
            self.main_window.show_appointments()
        else:
            messagebox.showinfo("Quick Action", "Navigate to Appointment Management section")
    
    def generate_invoices(self):
        """Quick action: Show invoice generation dialog"""
        try:
            # Get patients for invoice generation
            patients = self.db_manager.get_patients()
            if not patients:
                messagebox.showinfo("No Patients", "No patients found. Please add patients first.")
                return
            
            # Create a simple invoice dialog
            self.show_invoice_dialog(patients)
        except Exception as e:
            self.logger.error(f"Error generating invoices: {e}")
            messagebox.showerror("Error", f"Failed to generate invoices: {str(e)}")
    
    def view_calendar(self):
        """Quick action: Navigate to appointment management for calendar view"""
        if self.main_window:
            self.main_window.show_appointments()
        else:
            messagebox.showinfo("Quick Action", "Navigate to Appointment Management for calendar view")
    
    # Doctor Quick Actions
    def view_todays_appointments(self):
        """Quick action: Navigate to appointment management"""
        if self.main_window:
            self.main_window.show_appointments()
        else:
            messagebox.showinfo("Quick Action", "Navigate to Appointment Management to view today's appointments")
    
    def manage_medical_history(self):
        """Quick action: Navigate to medical history management"""
        if self.main_window:
            self.main_window.show_medical_history()
        else:
            messagebox.showinfo("Quick Action", "Navigate to Medical History Management section")
    
    def add_treatment_records(self):
        """Quick action: Navigate to treatment management"""
        if self.main_window:
            self.main_window.show_treatments()
        else:
            messagebox.showinfo("Quick Action", "Navigate to Treatment Management section")
    
    def patient_search(self):
        """Quick action: Navigate to patient management for search"""
        if self.main_window:
            self.main_window.show_patients()
        else:
            messagebox.showinfo("Quick Action", "Navigate to Patient Management for patient search")
    
    # Admin/General Quick Actions
    def view_treatments(self):
        """Quick action: Navigate to treatment management"""
        if self.main_window:
            self.main_window.show_treatments()
        else:
            messagebox.showinfo("Quick Action", "Navigate to Treatment Management section")
    
    def generate_reports(self):
        """Quick action: Navigate to reports section"""
        if self.main_window:
            self.main_window.show_reports()
        else:
            messagebox.showinfo("Quick Action", "Navigate to Reports section")
    
    def show_invoice_dialog(self, patients):
        """Show a simple invoice generation dialog"""
        # Create a new window for invoice generation
        invoice_window = tk.Toplevel(self)
        invoice_window.title("Generate Invoice")
        invoice_window.geometry("400x300")
        invoice_window.configure(bg='white')
        
        # Title
        title_label = tk.Label(
            invoice_window,
            text="Generate Invoice",
            font=('Arial', 16, 'bold'),
            bg='white'
        )
        title_label.pack(pady=20)
        
        # Patient selection
        tk.Label(invoice_window, text="Select Patient:", bg='white').pack(pady=5)
        patient_var = tk.StringVar()
        patient_combo = ttk.Combobox(
            invoice_window, 
            textvariable=patient_var,
            values=[f"{p['first_name']} {p['last_name']}" for p in patients],
            state="readonly",
            width=30
        )
        patient_combo.pack(pady=5)
        
        # Amount input
        tk.Label(invoice_window, text="Amount ($):", bg='white').pack(pady=5)
        amount_var = tk.StringVar()
        amount_entry = tk.Entry(invoice_window, textvariable=amount_var, width=30)
        amount_entry.pack(pady=5)
        
        # Notes input
        tk.Label(invoice_window, text="Notes:", bg='white').pack(pady=5)
        notes_text = tk.Text(invoice_window, height=3, width=30)
        notes_text.pack(pady=5)
        
        # Generate button
        def generate_invoice():
            try:
                selected_patient = patient_var.get()
                amount = amount_var.get()
                notes = notes_text.get(1.0, tk.END).strip()
                
                if not selected_patient or not amount:
                    messagebox.showwarning("Missing Information", "Please select a patient and enter an amount.")
                    return
                
                # Find the selected patient
                patient = None
                for p in patients:
                    if f"{p['first_name']} {p['last_name']}" == selected_patient:
                        patient = p
                        break
                
                if not patient:
                    messagebox.showerror("Error", "Selected patient not found.")
                    return
                
                # Create invoice data
                invoice_data = {
                    'patient_id': patient['id'],
                    'amount': float(amount),
                    'notes': notes,
                    'date': date.today().isoformat(),
                    'status': 'pending'
                }
                
                # Add invoice to database
                invoice_id = self.db_manager.add_invoice(invoice_data)
                
                messagebox.showinfo("Success", f"Invoice generated successfully!\nInvoice ID: {invoice_id}\nPatient: {selected_patient}\nAmount: ${amount}")
                invoice_window.destroy()
                
            except ValueError:
                messagebox.showerror("Invalid Amount", "Please enter a valid amount.")
            except Exception as e:
                self.logger.error(f"Error generating invoice: {e}")
                messagebox.showerror("Error", f"Failed to generate invoice: {str(e)}")
        
        generate_btn = tk.Button(
            invoice_window,
            text="Generate Invoice",
            command=generate_invoice,
            bg='#27ae60',
            fg='white',
            bd=0,
            padx=20,
            pady=8
        )
        generate_btn.pack(pady=20)
    
    def show_quick_patient_dialog(self):
        """Show a simplified patient addition dialog"""
        # Create a new window for quick patient addition
        patient_window = tk.Toplevel(self)
        patient_window.title("Quick Add Patient")
        patient_window.geometry("400x350")
        patient_window.configure(bg='white')
        
        # Title
        title_label = tk.Label(
            patient_window,
            text="Quick Add Patient",
            font=('Arial', 16, 'bold'),
            bg='white'
        )
        title_label.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(patient_window, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # First Name
        tk.Label(form_frame, text="First Name:", bg='white').grid(row=0, column=0, sticky=tk.W, pady=5)
        first_name_var = tk.StringVar()
        first_name_entry = tk.Entry(form_frame, textvariable=first_name_var, width=30)
        first_name_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Last Name
        tk.Label(form_frame, text="Last Name:", bg='white').grid(row=1, column=0, sticky=tk.W, pady=5)
        last_name_var = tk.StringVar()
        last_name_entry = tk.Entry(form_frame, textvariable=last_name_var, width=30)
        last_name_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Age
        tk.Label(form_frame, text="Age:", bg='white').grid(row=2, column=0, sticky=tk.W, pady=5)
        age_var = tk.StringVar()
        age_entry = tk.Entry(form_frame, textvariable=age_var, width=30)
        age_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Phone
        tk.Label(form_frame, text="Phone:", bg='white').grid(row=3, column=0, sticky=tk.W, pady=5)
        phone_var = tk.StringVar()
        phone_entry = tk.Entry(form_frame, textvariable=phone_var, width=30)
        phone_entry.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Treatment
        tk.Label(form_frame, text="Treatment:", bg='white').grid(row=4, column=0, sticky=tk.W, pady=5)
        treatment_var = tk.StringVar()
        treatment_entry = tk.Entry(form_frame, textvariable=treatment_var, width=30)
        treatment_entry.grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Add button
        def add_patient():
            try:
                # Validate required fields
                if not first_name_var.get().strip() or not last_name_var.get().strip():
                    messagebox.showwarning("Missing Information", "First Name and Last Name are required.")
                    return
                
                # Prepare patient data
                patient_data = {
                    'first_name': first_name_var.get().strip(),
                    'last_name': last_name_var.get().strip(),
                    'age': int(age_var.get()) if age_var.get().strip() else None,
                    'phone': phone_var.get().strip(),
                    'treatment': treatment_var.get().strip(),
                    'email': '',
                    'address': '',
                    'city': '',
                    'state': '',
                    'postal_code': '',
                    'emergency_contact_name': '',
                    'emergency_contact_phone': '',
                    'emergency_contact_relationship': '',
                    'assigned_doctor': None
                }
                
                # Auto-assign to doctor if available
                try:
                    doctors = self.db_manager.get_dentists()
                    if doctors:
                        patient_data['assigned_doctor'] = doctors[0]['username']
                except Exception as e:
                    self.logger.error(f"Error auto-assigning doctor: {e}")
                
                # Add patient to database
                patient_id = self.db_manager.add_patient(patient_data)
                
                messagebox.showinfo("Success", f"Patient added successfully!\nPatient ID: {patient_id}\nName: {patient_data['first_name']} {patient_data['last_name']}")
                patient_window.destroy()
                
                # Refresh dashboard data
                self.load_dashboard_data()
                
            except ValueError:
                messagebox.showerror("Invalid Age", "Please enter a valid age.")
            except Exception as e:
                self.logger.error(f"Error adding patient: {e}")
                messagebox.showerror("Error", f"Failed to add patient: {str(e)}")
        
        add_btn = tk.Button(
            patient_window,
            text="Add Patient",
            command=add_patient,
            bg='#27ae60',
            fg='white',
            bd=0,
            padx=20,
            pady=8
        )
        add_btn.pack(pady=20) 