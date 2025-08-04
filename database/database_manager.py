"""
Database Manager for Dental Clinic Management System
Handles all database operations using SQLite
"""

import sqlite3
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

class DatabaseManager:
    """Manages SQLite database operations for the dental clinic system"""
    
    def __init__(self, db_path: str = "dental_clinic.db"):
        """Initialize database manager with database file path"""
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        
    def get_connection(self) -> sqlite3.Connection:
        """Get a database connection"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            return conn
        except sqlite3.Error as e:
            self.logger.error(f"Database connection error: {e}")
            raise
    
    def initialize_database(self):
        """Create database tables if they don't exist"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Create users table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        role TEXT NOT NULL DEFAULT 'staff',
                        is_active BOOLEAN DEFAULT 1,
                        last_login TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        CHECK (role IN ('admin', 'dentist', 'hygienist', 'receptionist', 'staff'))
                    )
                ''')
                
                # Create patients table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS patients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        date_of_birth DATE,
                        gender TEXT CHECK (gender IN ('male', 'female', 'other', 'prefer_not_to_say')),
                        phone TEXT,
                        email TEXT,
                        address TEXT,
                        city TEXT,
                        state TEXT,
                        postal_code TEXT,
                        emergency_contact_name TEXT,
                        emergency_contact_phone TEXT,
                        emergency_contact_relationship TEXT,
                        medical_history TEXT,
                        allergies TEXT,
                        insurance_provider TEXT,
                        insurance_number TEXT,
                        insurance_group_number TEXT,
                        is_active BOOLEAN DEFAULT 1,
                        created_by INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (created_by) REFERENCES users (id)
                    )
                ''')
                
                # Create appointments table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS appointments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id INTEGER NOT NULL,
                        dentist_id INTEGER,
                        appointment_date DATE NOT NULL,
                        appointment_time TIME NOT NULL,
                        duration INTEGER DEFAULT 60,
                        appointment_type TEXT DEFAULT 'checkup',
                        treatment_plan TEXT,
                        notes TEXT,
                        status TEXT DEFAULT 'scheduled',
                        created_by INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (patient_id) REFERENCES patients (id),
                        FOREIGN KEY (dentist_id) REFERENCES users (id),
                        FOREIGN KEY (created_by) REFERENCES users (id),
                        CHECK (status IN ('scheduled', 'confirmed', 'in_progress', 'completed', 'cancelled', 'no_show')),
                        CHECK (appointment_type IN ('checkup', 'cleaning', 'filling', 'extraction', 'root_canal', 'crown', 'consultation', 'emergency', 'follow_up'))
                    )
                ''')
                
                # Create treatments table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS treatments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        category TEXT DEFAULT 'general',
                        duration INTEGER DEFAULT 60,
                        base_cost REAL NOT NULL,
                        is_active BOOLEAN DEFAULT 1,
                        created_by INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (created_by) REFERENCES users (id),
                        CHECK (category IN ('preventive', 'restorative', 'cosmetic', 'surgical', 'emergency', 'general'))
                    )
                ''')
                
                # Create treatment_records table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS treatment_records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id INTEGER NOT NULL,
                        treatment_id INTEGER NOT NULL,
                        appointment_id INTEGER,
                        dentist_id INTEGER,
                        treatment_date DATE NOT NULL,
                        treatment_notes TEXT,
                        actual_cost REAL NOT NULL,
                        payment_status TEXT DEFAULT 'pending',
                        completed_at TIMESTAMP,
                        created_by INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (patient_id) REFERENCES patients (id),
                        FOREIGN KEY (treatment_id) REFERENCES treatments (id),
                        FOREIGN KEY (appointment_id) REFERENCES appointments (id),
                        FOREIGN KEY (dentist_id) REFERENCES users (id),
                        FOREIGN KEY (created_by) REFERENCES users (id),
                        CHECK (payment_status IN ('pending', 'partial', 'paid', 'overdue', 'cancelled'))
                    )
                ''')
                
                # Create invoices table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS invoices (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        invoice_number TEXT UNIQUE NOT NULL,
                        patient_id INTEGER NOT NULL,
                        treatment_record_id INTEGER,
                        appointment_id INTEGER,
                        subtotal REAL NOT NULL DEFAULT 0.0,
                        tax_amount REAL NOT NULL DEFAULT 0.0,
                        discount_amount REAL NOT NULL DEFAULT 0.0,
                        total_amount REAL NOT NULL DEFAULT 0.0,
                        amount_paid REAL NOT NULL DEFAULT 0.0,
                        balance_due REAL NOT NULL DEFAULT 0.0,
                        invoice_date DATE NOT NULL,
                        due_date DATE NOT NULL,
                        status TEXT DEFAULT 'pending',
                        payment_terms TEXT DEFAULT 'Net 30',
                        notes TEXT,
                        created_by INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (patient_id) REFERENCES patients (id),
                        FOREIGN KEY (treatment_record_id) REFERENCES treatment_records (id),
                        FOREIGN KEY (appointment_id) REFERENCES appointments (id),
                        FOREIGN KEY (created_by) REFERENCES users (id),
                        CHECK (status IN ('draft', 'sent', 'paid', 'overdue', 'cancelled', 'refunded'))
                    )
                ''')
                
                # Create invoice_items table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS invoice_items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        invoice_id INTEGER NOT NULL,
                        treatment_record_id INTEGER,
                        description TEXT NOT NULL,
                        quantity INTEGER NOT NULL DEFAULT 1,
                        unit_price REAL NOT NULL,
                        total_price REAL NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (invoice_id) REFERENCES invoices (id),
                        FOREIGN KEY (treatment_record_id) REFERENCES treatment_records (id)
                    )
                ''')
                
                # Create payments table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS payments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        invoice_id INTEGER NOT NULL,
                        payment_date DATE NOT NULL,
                        payment_amount REAL NOT NULL,
                        payment_method TEXT NOT NULL,
                        payment_reference TEXT,
                        notes TEXT,
                        created_by INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (invoice_id) REFERENCES invoices (id),
                        FOREIGN KEY (created_by) REFERENCES users (id),
                        CHECK (payment_method IN ('cash', 'credit_card', 'debit_card', 'check', 'insurance', 'online', 'other'))
                    )
                ''')
                
                # Create indexes for better performance
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_patients_name ON patients(last_name, first_name)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(appointment_date)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_appointments_patient ON appointments(patient_id)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_treatment_records_patient ON treatment_records(patient_id)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_invoices_patient ON invoices(patient_id)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(status)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_payments_invoice ON payments(invoice_id)')
                
                conn.commit()
                self.logger.info("Database tables created successfully")
                
        except sqlite3.Error as e:
            self.logger.error(f"Database initialization error: {e}")
            raise
    
    # User Management Methods
    def add_user(self, user_data: Dict[str, Any]) -> int:
        """Add a new user to the database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (username, password_hash, first_name, last_name, email, role)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    user_data['username'],
                    user_data['password_hash'],
                    user_data['first_name'],
                    user_data['last_name'],
                    user_data['email'],
                    user_data.get('role', 'staff')
                ))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            self.logger.error(f"Error adding user: {e}")
            raise
    
    def get_users(self) -> List[Dict[str, Any]]:
        """Get all users"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users ORDER BY last_name, first_name')
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            self.logger.error(f"Error getting users: {e}")
            raise
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific user by ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except sqlite3.Error as e:
            self.logger.error(f"Error getting user by ID: {e}")
            raise
    
    def get_dentists(self) -> List[Dict[str, Any]]:
        """Get all dentists"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE role = "dentist" AND is_active = 1 ORDER BY last_name, first_name')
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            self.logger.error(f"Error getting dentists: {e}")
            raise
    
    # Patient Management Methods
    def add_patient(self, patient_data: Dict[str, Any]) -> int:
        """Add a new patient to the database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO patients (first_name, last_name, date_of_birth, gender, phone, email, 
                                        address, city, state, postal_code, emergency_contact_name,
                                        emergency_contact_phone, emergency_contact_relationship,
                                        medical_history, allergies, insurance_provider,
                                        insurance_number, insurance_group_number, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    patient_data['first_name'],
                    patient_data['last_name'],
                    patient_data.get('date_of_birth'),
                    patient_data.get('gender'),
                    patient_data.get('phone'),
                    patient_data.get('email'),
                    patient_data.get('address'),
                    patient_data.get('city'),
                    patient_data.get('state'),
                    patient_data.get('postal_code'),
                    patient_data.get('emergency_contact_name'),
                    patient_data.get('emergency_contact_phone'),
                    patient_data.get('emergency_contact_relationship'),
                    patient_data.get('medical_history'),
                    patient_data.get('allergies'),
                    patient_data.get('insurance_provider'),
                    patient_data.get('insurance_number'),
                    patient_data.get('insurance_group_number'),
                    patient_data.get('created_by')
                ))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            self.logger.error(f"Error adding patient: {e}")
            raise
    
    def get_patients(self, search_term: str = None) -> List[Dict[str, Any]]:
        """Get all patients or search by name"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if search_term:
                    cursor.execute('''
                        SELECT * FROM patients 
                        WHERE (first_name LIKE ? OR last_name LIKE ?) AND is_active = 1
                        ORDER BY last_name, first_name
                    ''', (f'%{search_term}%', f'%{search_term}%'))
                else:
                    cursor.execute('''
                        SELECT * FROM patients 
                        WHERE is_active = 1
                        ORDER BY last_name, first_name
                    ''')
                
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            self.logger.error(f"Error getting patients: {e}")
            raise
    
    def get_patient_by_id(self, patient_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific patient by ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except sqlite3.Error as e:
            self.logger.error(f"Error getting patient by ID: {e}")
            raise
    
    def update_patient(self, patient_id: int, patient_data: Dict[str, Any]) -> bool:
        """Update patient information"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE patients 
                    SET first_name = ?, last_name = ?, date_of_birth = ?, gender = ?, phone = ?, 
                        email = ?, address = ?, city = ?, state = ?, postal_code = ?,
                        emergency_contact_name = ?, emergency_contact_phone = ?, 
                        emergency_contact_relationship = ?, medical_history = ?, allergies = ?,
                        insurance_provider = ?, insurance_number = ?, insurance_group_number = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (
                    patient_data['first_name'],
                    patient_data['last_name'],
                    patient_data.get('date_of_birth'),
                    patient_data.get('gender'),
                    patient_data.get('phone'),
                    patient_data.get('email'),
                    patient_data.get('address'),
                    patient_data.get('city'),
                    patient_data.get('state'),
                    patient_data.get('postal_code'),
                    patient_data.get('emergency_contact_name'),
                    patient_data.get('emergency_contact_phone'),
                    patient_data.get('emergency_contact_relationship'),
                    patient_data.get('medical_history'),
                    patient_data.get('allergies'),
                    patient_data.get('insurance_provider'),
                    patient_data.get('insurance_number'),
                    patient_data.get('insurance_group_number'),
                    patient_id
                ))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            self.logger.error(f"Error updating patient: {e}")
            raise
    
    # Appointment Management Methods
    def add_appointment(self, appointment_data: Dict[str, Any]) -> int:
        """Add a new appointment"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO appointments (patient_id, dentist_id, appointment_date, appointment_time, 
                                            duration, appointment_type, treatment_plan, notes, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    appointment_data['patient_id'],
                    appointment_data.get('dentist_id'),
                    appointment_data['appointment_date'],
                    appointment_data['appointment_time'],
                    appointment_data.get('duration', 60),
                    appointment_data.get('appointment_type', 'checkup'),
                    appointment_data.get('treatment_plan'),
                    appointment_data.get('notes'),
                    appointment_data.get('created_by')
                ))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            self.logger.error(f"Error adding appointment: {e}")
            raise
    
    def get_appointments(self, date: str = None, patient_id: int = None) -> List[Dict[str, Any]]:
        """Get appointments with optional filtering"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = '''
                    SELECT a.*, p.first_name, p.last_name, u.username as dentist_name
                    FROM appointments a
                    JOIN patients p ON a.patient_id = p.id
                    LEFT JOIN users u ON a.dentist_id = u.id
                '''
                params = []
                
                if date:
                    query += ' WHERE a.appointment_date = ?'
                    params.append(date)
                elif patient_id:
                    query += ' WHERE a.patient_id = ?'
                    params.append(patient_id)
                
                query += ' ORDER BY a.appointment_date, a.appointment_time'
                
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            self.logger.error(f"Error getting appointments: {e}")
            raise
    
    def update_appointment_status(self, appointment_id: int, status: str) -> bool:
        """Update appointment status"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE appointments 
                    SET status = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (status, appointment_id))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            self.logger.error(f"Error updating appointment status: {e}")
            raise
    
    # Treatment Management Methods
    def get_treatments(self) -> List[Dict[str, Any]]:
        """Get all available treatments"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM treatments WHERE is_active = 1 ORDER BY name')
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            self.logger.error(f"Error getting treatments: {e}")
            raise
    
    def add_treatment(self, treatment_data: Dict[str, Any]) -> int:
        """Add a new treatment"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO treatments (name, description, category, duration, base_cost, created_by)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    treatment_data['name'],
                    treatment_data.get('description'),
                    treatment_data.get('category', 'general'),
                    treatment_data.get('duration', 60),
                    treatment_data['base_cost'],
                    treatment_data.get('created_by')
                ))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            self.logger.error(f"Error adding treatment: {e}")
            raise
    
    def add_treatment_record(self, record_data: Dict[str, Any]) -> int:
        """Add a new treatment record"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO treatment_records (patient_id, treatment_id, appointment_id, dentist_id,
                                                 treatment_date, treatment_notes, actual_cost, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    record_data['patient_id'],
                    record_data['treatment_id'],
                    record_data.get('appointment_id'),
                    record_data.get('dentist_id'),
                    record_data['treatment_date'],
                    record_data.get('treatment_notes'),
                    record_data['actual_cost'],
                    record_data.get('created_by')
                ))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            self.logger.error(f"Error adding treatment record: {e}")
            raise
    
    def get_patient_treatment_history(self, patient_id: int) -> List[Dict[str, Any]]:
        """Get treatment history for a specific patient"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT tr.*, t.name as treatment_name, t.description, u.username as dentist_name
                    FROM treatment_records tr
                    JOIN treatments t ON tr.treatment_id = t.id
                    LEFT JOIN users u ON tr.dentist_id = u.id
                    WHERE tr.patient_id = ?
                    ORDER BY tr.treatment_date DESC
                ''', (patient_id,))
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            self.logger.error(f"Error getting patient treatment history: {e}")
            raise
    
    # Invoice Management Methods
    def add_invoice(self, invoice_data: Dict[str, Any]) -> int:
        """Add a new invoice"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO invoices (invoice_number, patient_id, treatment_record_id, appointment_id,
                                        subtotal, tax_amount, discount_amount, total_amount,
                                        invoice_date, due_date, payment_terms, notes, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    invoice_data['invoice_number'],
                    invoice_data['patient_id'],
                    invoice_data.get('treatment_record_id'),
                    invoice_data.get('appointment_id'),
                    invoice_data.get('subtotal', 0.0),
                    invoice_data.get('tax_amount', 0.0),
                    invoice_data.get('discount_amount', 0.0),
                    invoice_data.get('total_amount', 0.0),
                    invoice_data['invoice_date'],
                    invoice_data['due_date'],
                    invoice_data.get('payment_terms', 'Net 30'),
                    invoice_data.get('notes'),
                    invoice_data.get('created_by')
                ))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            self.logger.error(f"Error adding invoice: {e}")
            raise
    
    def get_invoices(self, patient_id: int = None, status: str = None) -> List[Dict[str, Any]]:
        """Get invoices with optional filtering"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = '''
                    SELECT i.*, p.first_name, p.last_name
                    FROM invoices i
                    JOIN patients p ON i.patient_id = p.id
                '''
                params = []
                
                if patient_id:
                    query += ' WHERE i.patient_id = ?'
                    params.append(patient_id)
                elif status:
                    query += ' WHERE i.status = ?'
                    params.append(status)
                
                query += ' ORDER BY i.invoice_date DESC'
                
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            self.logger.error(f"Error getting invoices: {e}")
            raise
    
    def update_invoice_status(self, invoice_id: int, status: str) -> bool:
        """Update invoice status"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE invoices 
                    SET status = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (status, invoice_id))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            self.logger.error(f"Error updating invoice status: {e}")
            raise
    
    # Payment Management Methods
    def add_payment(self, payment_data: Dict[str, Any]) -> int:
        """Add a new payment"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO payments (invoice_id, payment_date, payment_amount, payment_method,
                                        payment_reference, notes, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    payment_data['invoice_id'],
                    payment_data['payment_date'],
                    payment_data['payment_amount'],
                    payment_data['payment_method'],
                    payment_data.get('payment_reference'),
                    payment_data.get('notes'),
                    payment_data.get('created_by')
                ))
                
                # Update invoice amount_paid and balance_due
                cursor.execute('''
                    UPDATE invoices 
                    SET amount_paid = amount_paid + ?, 
                        balance_due = total_amount - (amount_paid + ?),
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (payment_data['payment_amount'], payment_data['payment_amount'], payment_data['invoice_id']))
                
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            self.logger.error(f"Error adding payment: {e}")
            raise
    
    def get_payments(self, invoice_id: int = None) -> List[Dict[str, Any]]:
        """Get payments with optional filtering"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if invoice_id:
                    cursor.execute('SELECT * FROM payments WHERE invoice_id = ? ORDER BY payment_date DESC', (invoice_id,))
                else:
                    cursor.execute('SELECT * FROM payments ORDER BY payment_date DESC')
                
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            self.logger.error(f"Error getting payments: {e}")
            raise 