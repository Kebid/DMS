# Dental Clinic Management System

A comprehensive desktop application for managing dental clinic operations, built with Python, Tkinter, and SQLite.

## Features

- **Patient Management**: Add, edit, and manage patient records
- **Appointment Scheduling**: Schedule and manage appointments
- **Treatment Management**: Track treatments and procedures
- **Dashboard**: Overview of clinic operations and statistics
- **Database**: SQLite database for data persistence
- **Modern UI**: Clean and intuitive user interface

## Project Structure

```
DMS/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── database/              # Database management
│   ├── __init__.py
│   └── database_manager.py
├── models/                # Data models
│   ├── __init__.py
│   ├── patient.py
│   ├── appointment.py
│   └── treatment.py
├── ui/                    # User interface components
│   ├── __init__.py
│   ├── main_window.py
│   ├── dashboard_frame.py
│   ├── patient_frame.py
│   ├── appointment_frame.py
│   └── treatment_frame.py
└── utils/                 # Utility functions
    ├── __init__.py
    ├── logger.py
    └── validators.py
```

## Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd DMS
   ```

2. **Ensure Python is installed**
   - Python 3.7 or higher is required
   - The application uses only Python standard library modules

3. **Run the application**
   ```bash
   python main.py
   ```

## Usage

### Starting the Application
Run `python main.py` from the project directory. The application will:
- Initialize the SQLite database
- Create necessary tables
- Launch the main window

### Main Features

#### Dashboard
- View clinic statistics
- See today's appointments
- Quick access to common actions

#### Patient Management
- Add new patients with complete information
- Search and filter patient records
- Edit patient details
- View patient history

#### Appointment Management
- Schedule new appointments
- View appointments by date
- Update appointment status
- Manage appointment details

#### Treatment Management
- Define treatment types
- Set treatment costs and durations
- Track treatment records

## Database Schema

The application uses SQLite with the following main tables:

- **patients**: Patient information and medical history
- **appointments**: Appointment scheduling and status
- **treatments**: Available treatment types and costs
- **treatment_records**: Records of treatments performed
- **payments**: Payment tracking

## Configuration

### Database
- Database file: `dental_clinic.db` (created automatically)
- Location: Project root directory

### Logging
- Log files: `logs/dental_clinic.log`
- Log level: DEBUG for file, INFO for console

## Development

### Adding New Features
1. Create new model classes in `models/`
2. Add database methods in `database_manager.py`
3. Create UI components in `ui/`
4. Update main window to include new features

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Include docstrings for all functions and classes
- Handle exceptions appropriately

## Dependencies

The application uses only Python standard library modules:
- `tkinter`: GUI framework
- `sqlite3`: Database operations
- `datetime`: Date and time handling
- `logging`: Application logging
- `re`: Regular expressions
- `os`, `sys`: System operations
- `typing`: Type hints
- `dataclasses`: Data classes

## Optional Enhancements

To enable additional features, uncomment and install optional dependencies in `requirements.txt`:
- `pillow`: Image handling
- `reportlab`: PDF report generation
- `openpyxl`: Excel export
- `matplotlib`: Charts and graphs

## Troubleshooting

### Common Issues

1. **Database errors**
   - Ensure write permissions in the project directory
   - Check if database file is not locked by another process

2. **UI not displaying properly**
   - Ensure Tkinter is available (included with most Python installations)
   - Check screen resolution and scaling settings

3. **Import errors**
   - Ensure all Python files are in the correct directories
   - Check that `__init__.py` files are present in all packages

### Logs
Check the log file at `logs/dental_clinic.log` for detailed error information.

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs
3. Create an issue in the repository

---

**Note**: This is a basic implementation. For production use, consider adding:
- User authentication and authorization
- Data backup and recovery
- Advanced reporting features
- Integration with external systems
- Enhanced security measures 