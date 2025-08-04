"""
Treatment Frame for Dental Clinic Management System
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging

from models.treatment import Treatment

class TreatmentFrame(tk.Frame):
    """Treatment management frame"""
    
    def __init__(self, parent, db_manager):
        super().__init__(parent, bg='white')
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)
        self.selected_treatment = None
        
        self.setup_ui()
        self.load_treatments()
    
    def setup_ui(self):
        """Setup the treatment management user interface"""
        # Title
        title_label = tk.Label(
            self,
            text="Treatment Management",
            font=('Arial', 18, 'bold'),
            bg='white'
        )
        title_label.pack(pady=(20, 30))
        
        # Main content area
        content_frame = tk.Frame(self, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Left panel - Treatment list
        self.create_treatment_list_panel(content_frame)
        
        # Right panel - Treatment details
        self.create_treatment_details_panel(content_frame)
    
    def create_treatment_list_panel(self, parent):
        """Create the treatment list panel"""
        list_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Buttons frame
        buttons_frame = tk.Frame(list_frame, bg='white')
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        add_btn = tk.Button(
            buttons_frame,
            text="Add Treatment",
            command=self.add_treatment,
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
            command=self.load_treatments,
            bg='#3498db',
            fg='white',
            bd=0,
            padx=15,
            pady=5
        )
        refresh_btn.pack(side=tk.LEFT)
        
        # Treatment list
        list_label = tk.Label(list_frame, text="Treatments:", bg='white', font=('Arial', 12, 'bold'))
        list_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Treeview for treatment list
        self.treatment_tree = ttk.Treeview(
            list_frame,
            columns=('Name', 'Duration', 'Cost'),
            show='headings',
            height=15
        )
        
        self.treatment_tree.heading('Name', text='Treatment Name')
        self.treatment_tree.heading('Duration', text='Duration (min)')
        self.treatment_tree.heading('Cost', text='Cost ($)')
        
        self.treatment_tree.column('Name', width=200)
        self.treatment_tree.column('Duration', width=100)
        self.treatment_tree.column('Cost', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.treatment_tree.yview)
        self.treatment_tree.configure(yscrollcommand=scrollbar.set)
        
        self.treatment_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 10))
        
        # Bind selection event
        self.treatment_tree.bind('<<TreeviewSelect>>', self.on_treatment_select)
    
    def create_treatment_details_panel(self, parent):
        """Create the treatment details panel"""
        details_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Title
        details_title = tk.Label(
            details_frame,
            text="Treatment Details",
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
        """Create form fields for treatment details"""
        # Treatment Name
        tk.Label(parent, text="Treatment Name:", bg='white').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.name_var, width=30).grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Description
        tk.Label(parent, text="Description:", bg='white').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.description_text = tk.Text(parent, height=4, width=30)
        self.description_text.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Duration
        tk.Label(parent, text="Duration (min):", bg='white').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.duration_var = tk.StringVar(value="60")
        tk.Entry(parent, textvariable=self.duration_var, width=30).grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Cost
        tk.Label(parent, text="Cost ($):", bg='white').grid(row=3, column=0, sticky=tk.W, pady=5)
        self.cost_var = tk.StringVar()
        tk.Entry(parent, textvariable=self.cost_var, width=30).grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
    
    def create_action_buttons(self, parent):
        """Create action buttons"""
        buttons_frame = tk.Frame(parent, bg='white')
        buttons_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.save_btn = tk.Button(
            buttons_frame,
            text="Save",
            command=self.add_treatment,
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
            command=self.update_treatment,
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
            command=self.delete_treatment,
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
    
    def on_treatment_select(self, event):
        """Handle treatment selection"""
        selection = self.treatment_tree.selection()
        if selection:
            # Load treatment details (implementation needed)
            pass
    
    def load_treatments(self):
        """Load treatments from database"""
        try:
            # Clear existing items
            for item in self.treatment_tree.get_children():
                self.treatment_tree.delete(item)
            
            # Get treatments from database
            treatments = self.db_manager.get_treatments()
            
            # Add treatments to treeview
            for treatment in treatments:
                self.treatment_tree.insert('', tk.END, values=(
                    treatment['name'],
                    treatment['duration'],
                    f"${treatment['cost']:.2f}"
                ))
            
        except Exception as e:
            self.logger.error(f"Error loading treatments: {e}")
            messagebox.showerror("Error", f"Failed to load treatments: {str(e)}")
    
    def add_treatment(self):
        """Add a new treatment"""
        try:
            # Validate form data
            treatment_data = self.get_form_data()
            errors = self.validate_treatment_data(treatment_data)
            
            if errors:
                messagebox.showerror("Validation Error", "\n".join(errors))
                return
            
            # Add treatment to database (implementation needed in db_manager)
            # treatment_id = self.db_manager.add_treatment(treatment_data)
            
            messagebox.showinfo("Success", "Treatment added successfully")
            
            # Clear form and reload treatments
            self.clear_form()
            self.load_treatments()
            
        except Exception as e:
            self.logger.error(f"Error adding treatment: {e}")
            messagebox.showerror("Error", f"Failed to add treatment: {str(e)}")
    
    def update_treatment(self):
        """Update selected treatment"""
        if not self.selected_treatment:
            messagebox.showwarning("Warning", "Please select a treatment to update")
            return
        
        try:
            # Validate form data
            treatment_data = self.get_form_data()
            errors = self.validate_treatment_data(treatment_data)
            
            if errors:
                messagebox.showerror("Validation Error", "\n".join(errors))
                return
            
            # Update treatment in database (implementation needed)
            messagebox.showinfo("Success", "Treatment updated successfully")
            self.load_treatments()
            
        except Exception as e:
            self.logger.error(f"Error updating treatment: {e}")
            messagebox.showerror("Error", f"Failed to update treatment: {str(e)}")
    
    def delete_treatment(self):
        """Delete selected treatment"""
        if not self.selected_treatment:
            messagebox.showwarning("Warning", "Please select a treatment to delete")
            return
        
        # Confirm deletion
        result = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this treatment?")
        
        if result:
            try:
                # Delete treatment from database (implementation needed)
                messagebox.showinfo("Success", "Treatment deleted successfully")
                self.clear_form()
                self.load_treatments()
                
            except Exception as e:
                self.logger.error(f"Error deleting treatment: {e}")
                messagebox.showerror("Error", f"Failed to delete treatment: {str(e)}")
    
    def clear_form(self):
        """Clear the form fields"""
        self.selected_treatment = None
        
        # Clear all form variables
        self.name_var.set('')
        self.duration_var.set('60')
        self.cost_var.set('')
        
        # Clear text fields
        self.description_text.delete(1.0, tk.END)
        
        # Disable update and delete buttons
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
    
    def get_form_data(self):
        """Get data from form fields"""
        return {
            'name': self.name_var.get().strip(),
            'description': self.description_text.get(1.0, tk.END).strip(),
            'duration': int(self.duration_var.get()) if self.duration_var.get() else 60,
            'cost': float(self.cost_var.get()) if self.cost_var.get() else 0.0
        }
    
    def validate_treatment_data(self, data):
        """Validate treatment data"""
        errors = []
        
        if not data['name']:
            errors.append("Treatment name is required")
        
        if data['duration'] <= 0:
            errors.append("Duration must be greater than 0")
        
        if data['cost'] < 0:
            errors.append("Cost cannot be negative")
        
        return errors 