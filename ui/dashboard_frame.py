"""
Dashboard Frame for Dental Clinic Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
import logging

class DashboardFrame(tk.Frame):
    """Dashboard frame showing role-specific overview information"""
    
    def __init__(self, parent, db_manager, current_user=None):
        super().__init__(parent, bg='white')
        self.db_manager = db_manager
        self.current_user = current_user
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
                ("Manage Patients", self.manage_patients, "#3498db"),
                ("Schedule Appointments", self.schedule_appointments, "#e74c3c"),
                ("Generate Invoices", self.generate_invoices, "#9b59b6"),
                ("View Calendar", self.view_calendar, "#f39c12")
            ]
        elif role == 'dentist':
            actions = [
                ("View Today's Appointments", self.view_todays_appointments, "#e74c3c"),
                ("View Patient History", self.view_patient_history, "#3498db"),
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
    def manage_patients(self):
        """Quick action: Manage patients"""
        messagebox.showinfo("Quick Action", "Manage Patients functionality will be implemented in the Patient Management section.")
    
    def schedule_appointments(self):
        """Quick action: Schedule appointments"""
        messagebox.showinfo("Quick Action", "Schedule Appointments functionality will be implemented in the Appointment Management section.")
    
    def generate_invoices(self):
        """Quick action: Generate invoices"""
        messagebox.showinfo("Quick Action", "Generate Invoices functionality will be implemented in the Invoice Management section.")
    
    def view_calendar(self):
        """Quick action: View calendar"""
        messagebox.showinfo("Quick Action", "View Calendar functionality will be implemented in the Appointment Management section.")
    
    # Dentist Quick Actions
    def view_todays_appointments(self):
        """Quick action: View today's appointments"""
        messagebox.showinfo("Quick Action", "Today's appointments are displayed above. Detailed view will be implemented in the Appointment Management section.")
    
    def view_patient_history(self):
        """Quick action: View patient history"""
        messagebox.showinfo("Quick Action", "View Patient History functionality will be implemented in the Patient Management section.")
    
    def add_treatment_records(self):
        """Quick action: Add treatment records"""
        messagebox.showinfo("Quick Action", "Add Treatment Records functionality will be implemented in the Treatment Management section.")
    
    def patient_search(self):
        """Quick action: Patient search"""
        messagebox.showinfo("Quick Action", "Patient Search functionality will be implemented in the Patient Management section.")
    
    # Admin/General Quick Actions
    def view_treatments(self):
        """Quick action: View treatments"""
        messagebox.showinfo("Quick Action", "View Treatments functionality will be implemented in the Treatment Management section.")
    
    def generate_reports(self):
        """Quick action: Generate reports"""
        messagebox.showinfo("Quick Action", "Generate Reports functionality will be implemented in the Reports section.") 