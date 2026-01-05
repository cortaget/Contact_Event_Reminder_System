README.md - Event Reminder System

Based on all the information from our conversation, here's a comprehensive README in English:
📅 Event Reminder System

Personal Contacts & Events Manager with Automatic Reminders

A desktop application for managing contacts, events, and automated reminders built with Python, CustomTkinter, and SQL Server.
🌟 Features
Core Functionality

    Contact Management - Store and organize personal information (name, birth date, gender)

    Event Tracking - Track birthdays, anniversaries, and custom events

    Group Organization - Categorize contacts into groups (Family, Friends, Work)

    Automatic Reminders - Background notification system with hourly checks

    Smart Filtering - Filter events by timeframe (30 days, 90 days, all)

    Reports & Statistics - Generate summaries and upcoming events reports

    CSV Import - Bulk import contacts from CSV files

Technical Features

    Database Auto-Initialization - First-run wizard creates database structure automatically

    Configuration Manager - Easy database connection setup via GUI

    Data Integrity - Cascading deletes and foreign key relationships

    Modern UI - Dark theme with CustomTkinter framework

    Background Processing - Thread-safe reminder system running in background

💻 System Requirements
Minimum Requirements

    OS: Windows 10/11 (64-bit)

    RAM: 2 GB

    Disk Space: 200 MB

    Database: Microsoft SQL Server 2016+ or SQL Server Express

    ODBC Driver: ODBC Driver 17 for SQL Server

Recommended

    RAM: 4 GB or more

    SQL Server: SQL Server 2019+

    ODBC Driver: ODBC Driver 18 for SQL Server

🚀 Installation
Step 1: Install SQL Server

    Download SQL Server Express (free): https://www.microsoft.com/sql-server/sql-server-downloads

    Install with default settings

    Note your server name (usually localhost\SQLEXPRESS or .)

Step 2: Install ODBC Driver

    Download ODBC Driver 17 for SQL Server: https://go.microsoft.com/fwlink/?linkid=2249004

    Run installer and complete setup

Step 3: Install Application

    Download Event_Reminder_System.exe

    Place in desired folder (e.g., C:\Program Files\EventReminder\)

    Double-click to launch

Step 4: First Run Setup

    Application detects missing database automatically

    Click "Create Database" in setup dialog

    Wait 15-30 seconds for initialization

    Click "Close" when complete

📖 Usage Guide
Adding Contacts

    Click "Osoby" (Contacts) in left menu

    Click "+ Přidat" (Add)

    Fill in: First Name, Last Name, Birth Date (optional), Gender (optional)

    Click "Uložit" (Save)

Creating Events

    Click "Události" (Events) in left menu

    Click "+ Přidat" (Add)

    Select person from dropdown

    Choose event type (Birthday, Anniversary, etc.)

    Set event date and reminder preferences

    Click "Uložit" (Save)

Creating Groups

    Click "Skupiny" (Groups) in left menu

    Click "+ Přidat" (Add)

    Enter group name

    Click "Uložit" (Save)

    Add members using "Přidat členy" button

Reminder System

The application automatically:

    Checks for upcoming events every 1 hour (background thread)

    Shows popup notifications when events require attention

    Displays event cards with color-coded urgency (red=today, orange=tomorrow, blue=3-7 days)

⚙️ Configuration
Configuration File (config.json)

Located in the same folder as the EXE file:

json
{
    "database": {
        "server": ".",
        "database": "Contact_Event_Reminder_System",
        "driver": "ODBC Driver 17 for SQL Server",
        "trusted_connection": true
    },
    "settings": {
        "default_reminder_days": 7
    }
}

Common Server Names

    Local SQL Express: localhost\SQLEXPRESS or .\SQLEXPRESS

    Local SQL Server: localhost or .

    Remote Server: 192.168.1.100 or ServerName

Changing Settings

Method 1: Via GUI

    Click "Nastavení" (Settings)

    Modify server/database values

    Click "Test Connection"

    Click "Save"

Method 2: Edit config.json

    Close application

    Edit config.json in text editor

    Save and restart application

🔨 Building from Source
Prerequisites

bash
pip install customtkinter pyodbc pyinstaller

Build EXE

bash
python build_exe.py

Output: dist/Event_Reminder_System.exe
📁 Project Structure

text
Event_Reminder_System/
├── main.py                          # Application entry point
├── config.py                        # Configuration manager
├── database_initializer.py          # Database setup logic
├── build_exe.py                     # PyInstaller build script
├── ui/
│   ├── main_window.py              # Main application window
│   ├── dashboard_screen.py         # Dashboard UI
│   ├── persons_screen.py           # Contacts management
│   ├── events_screen.py            # Events management
│   ├── groups_screen.py            # Groups management
│   ├── database_setup_window.py    # DB initialization wizard
│   └── reminder_notification_window.py  # Reminder popup
├── services/
│   └── notification_service.py     # Reminder system logic
├── repositories/
│   ├── person_repository.py        # Contact data access
│   ├── event_repository.py         # Event data access
│   └── group_repository.py         # Group data access
└── config.json                      # Configuration file (auto-generated)

🗄️ Database Schema
Tables (7)

    person - Contact information

    event - Event records linked to contacts

    event_type - Event categories (Birthday, Anniversary, etc.)

    group - Group definitions

    person_group - Many-to-many relationship between persons and groups

    notification - Notification history (planned, sent, failed)

    user - User settings (future use)

Views (3)

    v_upcoming_events - Events in the future with days remaining

    v_event_summary - Events categorized by time (today, this week, this month)

    v_group_statistics - Group member and event counts

🛠️ Technologies Used

    Python 3.12 - Core language

    CustomTkinter - Modern UI framework

    pyodbc - SQL Server database connectivity

    SQL Server - Relational database

    PyInstaller - EXE packaging

    Threading - Background reminder system

🐛 Troubleshooting
Application won't start

    Verify SQL Server is running (services.msc → SQL Server (SQLEXPRESS))

    Check ODBC Driver is installed (odbcad32.exe)

    Review config.json settings

Connection failed

    Test server name in command line: sqlcmd -S localhost\SQLEXPRESS -E

    Ensure Windows Authentication is enabled

    Check firewall settings for SQL Server

Reminders not showing

    Verify event date is today or in future

    Check reminder_days_before setting

    Ensure event date is within reminder window

📝 License

This project is created for educational purposes as part of a school assignment.
👤 Author

Created in January 2026 as a school project for contact and event management with automated reminders.
🙏 Acknowledgments

    CustomTkinter for modern UI components

    Microsoft SQL Server for robust database management

    Python community for excellent libraries

Version: 1.0
Last Updated: January 5, 2026