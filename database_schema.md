# Dental Clinic Management System - Database Schema

## Overview
This document describes the complete SQLite database schema for the Dental Clinic Management System, including all tables, fields, relationships, and constraints.

## Database Tables

### 1. Users Table
**Purpose**: Store system users (staff, dentists, administrators)

```sql
CREATE TABLE users (
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
);
```

**Fields**:
- `id`: Primary key, auto-incrementing
- `username`: Unique username for login
- `password_hash`: Hashed password for security
- `first_name`, `last_name`: User's full name
- `email`: Unique email address
- `role`: User role with constraints
- `is_active`: Boolean flag for active/inactive users
- `last_login`: Timestamp of last login
- `created_at`, `updated_at`: Audit timestamps

### 2. Patients Table
**Purpose**: Store patient information and medical history

```sql
CREATE TABLE patients (
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
);
```

**Fields**:
- `id`: Primary key, auto-incrementing
- `first_name`, `last_name`: Patient's full name
- `date_of_birth`: Patient's birth date
- `gender`: Gender with constraint options
- `phone`, `email`: Contact information
- `address`, `city`, `state`, `postal_code`: Complete address
- `emergency_contact_*`: Emergency contact details
- `medical_history`: Medical history notes
- `allergies`: Known allergies
- `insurance_*`: Insurance information
- `is_active`: Boolean flag for active/inactive patients
- `created_by`: Foreign key to users table
- `created_at`, `updated_at`: Audit timestamps

### 3. Appointments Table
**Purpose**: Store appointment scheduling information

```sql
CREATE TABLE appointments (
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
);
```

**Fields**:
- `id`: Primary key, auto-incrementing
- `patient_id`: Foreign key to patients table
- `dentist_id`: Foreign key to users table (dentist)
- `appointment_date`, `appointment_time`: Date and time of appointment
- `duration`: Duration in minutes (default 60)
- `appointment_type`: Type of appointment with constraints
- `treatment_plan`: Planned treatment details
- `notes`: Additional notes
- `status`: Appointment status with constraints
- `created_by`: Foreign key to users table
- `created_at`, `updated_at`: Audit timestamps

### 4. Treatments Table
**Purpose**: Store available treatment types and their base costs

```sql
CREATE TABLE treatments (
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
);
```

**Fields**:
- `id`: Primary key, auto-incrementing
- `name`: Treatment name
- `description`: Treatment description
- `category`: Treatment category with constraints
- `duration`: Standard duration in minutes
- `base_cost`: Base cost for the treatment
- `is_active`: Boolean flag for active/inactive treatments
- `created_by`: Foreign key to users table
- `created_at`, `updated_at`: Audit timestamps

### 5. Treatment Records Table
**Purpose**: Store actual treatments performed on patients

```sql
CREATE TABLE treatment_records (
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
);
```

**Fields**:
- `id`: Primary key, auto-incrementing
- `patient_id`: Foreign key to patients table
- `treatment_id`: Foreign key to treatments table
- `appointment_id`: Optional foreign key to appointments table
- `dentist_id`: Foreign key to users table (dentist who performed treatment)
- `treatment_date`: Date treatment was performed
- `treatment_notes`: Notes about the treatment
- `actual_cost`: Actual cost charged (may differ from base_cost)
- `payment_status`: Payment status with constraints
- `completed_at`: Timestamp when treatment was completed
- `created_by`: Foreign key to users table
- `created_at`, `updated_at`: Audit timestamps

### 6. Invoices Table
**Purpose**: Store billing information for treatments

```sql
CREATE TABLE invoices (
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
);
```

**Fields**:
- `id`: Primary key, auto-incrementing
- `invoice_number`: Unique invoice number
- `patient_id`: Foreign key to patients table
- `treatment_record_id`: Optional foreign key to treatment_records table
- `appointment_id`: Optional foreign key to appointments table
- `subtotal`: Subtotal before tax and discounts
- `tax_amount`: Tax amount
- `discount_amount`: Discount amount
- `total_amount`: Total amount after tax and discounts
- `amount_paid`: Amount already paid
- `balance_due`: Remaining balance
- `invoice_date`: Date invoice was created
- `due_date`: Payment due date
- `status`: Invoice status with constraints
- `payment_terms`: Payment terms (default "Net 30")
- `notes`: Additional notes
- `created_by`: Foreign key to users table
- `created_at`, `updated_at`: Audit timestamps

### 7. Invoice Items Table
**Purpose**: Store individual line items on invoices

```sql
CREATE TABLE invoice_items (
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
);
```

**Fields**:
- `id`: Primary key, auto-incrementing
- `invoice_id`: Foreign key to invoices table
- `treatment_record_id`: Optional foreign key to treatment_records table
- `description`: Item description
- `quantity`: Quantity (default 1)
- `unit_price`: Price per unit
- `total_price`: Total price for this item
- `created_at`: Creation timestamp

### 8. Payments Table
**Purpose**: Store payment records for invoices

```sql
CREATE TABLE payments (
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
);
```

**Fields**:
- `id`: Primary key, auto-incrementing
- `invoice_id`: Foreign key to invoices table
- `payment_date`: Date payment was received
- `payment_amount`: Amount paid
- `payment_method`: Method of payment with constraints
- `payment_reference`: Reference number or check number
- `notes`: Additional notes
- `created_by`: Foreign key to users table
- `created_at`: Creation timestamp

## Database Indexes

The following indexes are created for better query performance:

```sql
CREATE INDEX idx_patients_name ON patients(last_name, first_name);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);
CREATE INDEX idx_appointments_patient ON appointments(patient_id);
CREATE INDEX idx_treatment_records_patient ON treatment_records(patient_id);
CREATE INDEX idx_invoices_patient ON invoices(patient_id);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_payments_invoice ON payments(invoice_id);
```

## Relationships

### Primary Relationships:
1. **Users → Patients**: One user can create many patients
2. **Users → Appointments**: One user (dentist) can have many appointments
3. **Patients → Appointments**: One patient can have many appointments
4. **Patients → Treatment Records**: One patient can have many treatment records
5. **Treatments → Treatment Records**: One treatment type can be used in many records
6. **Appointments → Treatment Records**: One appointment can have one treatment record
7. **Treatment Records → Invoices**: One treatment record can have one invoice
8. **Invoices → Invoice Items**: One invoice can have many invoice items
9. **Invoices → Payments**: One invoice can have many payments

### Foreign Key Constraints:
- All foreign keys are properly defined with REFERENCES clauses
- Cascade operations are not implemented (manual handling required)
- NULL values are allowed for optional relationships

## Data Integrity

### Constraints:
- **NOT NULL**: Required fields are marked as NOT NULL
- **UNIQUE**: Username and email in users table, invoice_number in invoices table
- **CHECK**: Enumerated values for status fields, roles, and categories
- **DEFAULT**: Sensible default values for common fields
- **FOREIGN KEY**: All relationships are properly constrained

### Validation Rules:
- Appointment status must be one of the defined values
- Payment status must be one of the defined values
- User roles must be one of the defined values
- Treatment categories must be one of the defined values
- Payment methods must be one of the defined values

## Audit Trail

### Timestamp Fields:
- `created_at`: When the record was created
- `updated_at`: When the record was last modified
- `last_login`: Last login time for users
- `completed_at`: When treatment was completed
- `payment_date`: When payment was received

### User Tracking:
- `created_by`: User who created the record
- `dentist_id`: Dentist who performed treatment or appointment
- All major operations are tracked to the user level

## Security Considerations

1. **Password Hashing**: Passwords are stored as hashes, not plain text
2. **User Roles**: Role-based access control with defined roles
3. **Active/Inactive Flags**: Soft delete capability for users and patients
4. **Audit Trail**: Complete tracking of who created/modified records
5. **Input Validation**: Constraints prevent invalid data entry

## Performance Considerations

1. **Indexes**: Strategic indexes on frequently queried fields
2. **Normalization**: Proper normalization to reduce data redundancy
3. **Foreign Keys**: Efficient relationship lookups
4. **Soft Deletes**: Maintains referential integrity while allowing "deletion"

## Backup and Recovery

The SQLite database file (`dental_clinic.db`) should be backed up regularly:
- Full database backup before major updates
- Incremental backups for data changes
- Test restore procedures regularly
- Consider using SQLite's built-in backup API for large databases 