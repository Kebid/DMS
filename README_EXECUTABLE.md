# 🦷 Dental Clinic Management System - Executable Version

## 📦 Installation & Usage

### **Quick Start:**
1. **Download** the `DentalClinicManager.exe` file
2. **Double-click** to run the application
3. **Login** with your credentials

### **System Requirements:**
- **Windows 10/11** (64-bit)
- **No Python installation required** (standalone executable)
- **Minimum 100MB free disk space**
- **4GB RAM recommended**

---

## 🔐 **Default Login Credentials:**

### **Receptionist Account:**
- **Username:** `receptionist`
- **Password:** `recep123`

### **Doctor Account:**
- **Username:** `doctor`
- **Password:** `doctor123`

---

## 🏥 **Features:**

### **👩‍💼 Receptionist Features:**
- ✅ **Patient Management**: Add, edit, delete patients
- ✅ **Quick Add Patient**: Simplified patient addition
- ✅ **Generate Invoices**: Create invoices for patients
- ✅ **View Medical History**: Read-only access to patient treatments
- ✅ **Appointment Management**: Schedule and manage appointments

### **👨‍⚕️ Doctor Features:**
- ✅ **Medical History Management**: Add treatments with costs
- ✅ **Patient Overview**: View patient information (read-only)
- ✅ **Treatment Records**: Track patient treatments and costs
- ✅ **Today's Appointments**: View scheduled appointments

### **🎯 Quick Actions:**
- **Role-based quick access** to common tasks
- **One-click navigation** to different sections
- **Direct functionality** for common operations

---

## 💾 **Data Storage:**

- **Database**: SQLite database (`clinic.db`) created automatically
- **Location**: Same folder as the executable
- **Backup**: Copy the `.db` file to backup your data
- **Portable**: Database travels with the executable

---

## 🚀 **Running the Application:**

### **Method 1: Direct Execution**
```
Double-click: DentalClinicManager.exe
```

### **Method 2: Command Line**
```cmd
DentalClinicManager.exe
```

### **Method 3: Batch File**
```
Double-click: run_dental_clinic.bat
```

---

## 🔧 **Troubleshooting:**

### **Application Won't Start:**
1. **Check Windows Defender**: May block the executable
2. **Run as Administrator**: Right-click → "Run as administrator"
3. **Check Antivirus**: Add to exceptions if blocked

### **Database Issues:**
1. **Check Permissions**: Ensure write access to folder
2. **Check Disk Space**: Ensure sufficient free space
3. **Restart Application**: Close and reopen if needed

### **Login Problems:**
1. **Verify Credentials**: Use exact username/password
2. **Check Caps Lock**: Ensure correct case
3. **Database Reset**: Delete `clinic.db` to reset (loses all data)

---

## 📁 **File Structure:**

```
DentalClinicManager/
├── DentalClinicManager.exe    # Main executable
├── run_dental_clinic.bat      # Batch file for easy launch
├── clinic.db                  # Database (created automatically)
└── README_EXECUTABLE.md       # This file
```

---

## 🆘 **Support:**

### **Common Issues:**
- **"Application blocked"**: Add to Windows Defender exclusions
- **"Database error"**: Check folder permissions
- **"Login failed"**: Verify credentials or reset database

### **Data Backup:**
- **Copy `clinic.db`** to backup location
- **Database contains**: All patients, appointments, medical history
- **Portable**: Can be moved to another computer

---

## 🎉 **Success!**

Your Dental Clinic Management System is now ready to use as a standalone Windows application!

**No Python installation required** - everything is packaged into the executable.

---

*Built with PyInstaller - Professional Python Application Packaging* 