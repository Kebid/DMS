"""
Medical History Frame for Dental Clinic Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import logging

class MedicalHistoryFrame(tk.Frame):
    """Medical history management frame for doctors"""
    
    def __init__(self, parent, db_manager, current_user=None, patient_id=None):
        super().__init__(parent, bg='white')
        self.db_manager = db_manager
        self.current_user = current_user
        self.patient_id = patient_id
        self.logger = logging.getLogger(__name__)
        
        self.setup_ui()
        if patient_id:
            self.load_medical_history()
    
    def setup_ui(self):
        """Setup the medical history management user interface"""
        # Title
        title_label = tk.Label(
            self,
            text="Medical History Management",
            font=('Arial', 18, 'bold'),
            bg='white'
        )
        title_label.pack(pady=(20, 30))
        
        # Main content area
        content_frame = tk.Frame(self, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Left panel - Medical history list
        self.create_history_list_panel(content_frame)
        
        # Right panel - Add new entry
        self.create_add_entry_panel(content_frame)
    
    def create_history_list_panel(self, parent):
        """Create the medical history list panel"""
        list_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Title
        list_label = tk.Label(list_frame, text="Medical History:", bg='white', font=('Arial', 12, 'bold'))
        list_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Treeview for medical history list
        self.history_tree = ttk.Treeview(
            list_frame,
            columns=('Date', 'Treatment', 'Cost', 'Notes'),
            show='headings',
            height=15
        )
        
        self.history_tree.heading('Date', text='Date')
        self.history_tree.heading('Treatment', text='Treatment')
        self.history_tree.heading('Cost', text='Cost')
        self.history_tree.heading('Notes', text='Notes')
        
        self.history_tree.column('Date', width=100)
        self.history_tree.column('Treatment', width=150)
        self.history_tree.column('Cost', width=80)
        self.history_tree.column('Notes', width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 10))
    
    def create_add_entry_panel(self, parent):
        """Create the add new entry panel"""
        add_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        add_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Title
        add_title = tk.Label(
            add_frame,
            text="Add New Entry",
            font=('Arial', 14, 'bold'),
            bg='white'
        )
        add_title.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(add_frame, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Date
        tk.Label(form_frame, text="Date:", bg='white').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.date_var = tk.StringVar(value=date.today().isoformat())
        tk.Entry(form_frame, textvariable=self.date_var, width=30).grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Treatment
        tk.Label(form_frame, text="Treatment:", bg='white').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.treatment_var = tk.StringVar()
        treatment_combo = ttk.Combobox(form_frame, textvariable=self.treatment_var, width=27, state="readonly")
        treatment_combo['values'] = ['Checkup', 'Cleaning', 'Filling', 'Root Canal', 'Extraction', 'Crown', 'Consultation', 'Emergency', 'Follow-up']
        treatment_combo.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Cost
        tk.Label(form_frame, text="Cost ($):", bg='white').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.cost_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.cost_var, width=30).grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Notes
        tk.Label(form_frame, text="Notes:", bg='white').grid(row=3, column=0, sticky=tk.W, pady=5)
        self.notes_text = tk.Text(form_frame, height=4, width=30)
        self.notes_text.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Add button
        add_btn = tk.Button(
            add_frame,
            text="Add Entry",
            command=self.add_medical_history_entry,
            bg='#27ae60',
            fg='white',
            bd=0,
            padx=20,
            pady=8
        )
        add_btn.pack(pady=20)
    
    def load_medical_history(self):
        """Load medical history from database"""
        try:
            # Clear existing items
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)
            
            if not self.patient_id:
                return
            
            # Get medical history from database
            medical_history = self.db_manager.get_medical_history(self.patient_id)
            
            # Add entries to treeview
            for entry in medical_history:
                # Parse the note to extract treatment and cost
                note = entry.get('note', '')
                treatment = "General"
                cost = "$0"
                
                # Try to extract treatment and cost from note
                if "Treatment:" in note and "Cost:" in note:
                    parts = note.split("Cost:")
                    if len(parts) == 2:
                        treatment_part = parts[0].replace("Treatment:", "").strip()
                        cost_part = parts[1].strip()
                        treatment = treatment_part
                        cost = cost_part
                
                self.history_tree.insert('', tk.END, values=(
                    entry.get('date', ''),
                    treatment,
                    cost,
                    note
                ))
            
        except Exception as e:
            self.logger.error(f"Error loading medical history: {e}")
            messagebox.showerror("Error", f"Failed to load medical history: {str(e)}")
    
    def add_medical_history_entry(self):
        """Add a new medical history entry"""
        try:
            # Validate form data
            if not self.treatment_var.get().strip():
                messagebox.showerror("Error", "Please select a treatment")
                return
            
            if not self.cost_var.get().strip():
                messagebox.showerror("Error", "Please enter a cost")
                return
            
            # Create the note with treatment and cost
            treatment = self.treatment_var.get().strip()
            cost = self.cost_var.get().strip()
            notes = self.notes_text.get(1.0, tk.END).strip()
            
            note_text = f"Treatment: {treatment} Cost: ${cost}"
            if notes:
                note_text += f" Notes: {notes}"
            
            # Prepare data
            history_data = {
                'patient_id': self.patient_id,
                'note': note_text,
                'date': self.date_var.get().strip(),
                'created_by': self.current_user.get('id') if self.current_user else None
            }
            
            # Add to database
            entry_id = self.db_manager.add_medical_history(history_data)
            
            messagebox.showinfo("Success", f"Medical history entry added successfully")
            
            # Clear form
            self.treatment_var.set('')
            self.cost_var.set('')
            self.notes_text.delete(1.0, tk.END)
            
            # Reload medical history
            self.load_medical_history()
            
        except Exception as e:
            self.logger.error(f"Error adding medical history entry: {e}")
            messagebox.showerror("Error", f"Failed to add medical history entry: {str(e)}") 