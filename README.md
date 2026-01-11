# 📅 EVENT REMINDER SYSTEM
### Personal Contacts & Events Manager with Automatic Reminders

---

## 📋 PROJECT INFORMATION

| Field | Value |
|-------|-------|
| **Project Name** | Event Reminder System |
| **Author** | [ТВОЁ ИМЯ] |
| **Email** | [ТВОЙ EMAIL] |
| **School** | [НАЗВАНИЕ ШКОЛЫ] |
| **Course** | Databázové systémy |
| **Date** | 11.01.2026 |
| **Version** | 1.0 |
| **Type** | 🎓 School Project |

---

## 📖 TABLE OF CONTENTS

1. [Executive Summary](#1-executive-summary)
2. [User Requirements](#2-user-requirements)
3. [System Architecture](#3-system-architecture)
4. [Database Design](#4-database-design)
5. [Application Behavior](#5-application-behavior)
6. [Configuration](#6-configuration)
7. [Installation Guide](#7-installation-guide)
8. [Error Handling](#8-error-handling)
9. [Third-Party Libraries](#9-third-party-libraries)
10. [Project Conclusion](#10-project-conclusion)

---

## 1. EXECUTIVE SUMMARY

### 1.1 Project Overview

Event Reminder System je desktopová aplikace pro správu osobních kontaktů a důležitých událostí s automatickým systémem připomínek. Aplikace sleduje narozeniny, výročí a vlastní události, zajišťuje včasná upozornění a pomáhá udržovat kontakty s důležitými lidmi.

### 1.2 Key Features

| Feature | Description |
|---------|-------------|
| 👤 **Contact Management** | Uchovávání osobních informací (jméno, datum narození, pohlaví) |
| 📅 **Event Tracking** | Sledování narozenin, výročí a vlastních událostí |
| 🔔 **Automated Reminders** | Automatické kontroly každou hodinu s vyskakovacími upozorněními |
| 👥 **Group Organization** | Kategorizace kontaktů do skupin (rodina, prátelé, práce) |
| 📥 **CSV Import** | Hromadný import kontaktů ze souborů |
| 📊 **Reports** | Statistiky a přehledy nadcházejících událostí |

### 1.3 Technology Stack

┌─────────────────────────────────┐
│ Frontend: CustomTkinter 5.2.2 │
│ Language: Python 3.10+ │
│ Database: MS SQL Server 2016+ │
│ Driver: ODBC Driver 17 │
│ Architecture: Desktop App │
└─────────────────────────────────┘

text

---

## 2. USER REQUIREMENTS

### 2.1 Use Case Diagram

```mermaid
graph TD
    User((User))
    
    User --> UC1[Manage Contacts]
    User --> UC2[Manage Events]
    User --> UC3[View Reminders]
    User --> UC4[Manage Groups]
    User --> UC5[Import Data]
    
    UC1 --> UC1A[Add Contact]
    UC1 --> UC1B[Edit Contact]
    UC1 --> UC1C[Delete Contact]
    
    UC2 --> UC2A[Create Event]
    UC2 --> UC2B[Set Reminder]
    UC2 --> UC2C[Edit Event]
    
    UC3 --> UC3A[Acknowledge]
    UC3 --> UC3B[Postpone]
    
    UC4 --> UC4A[Create Group]
    UC4 --> UC4B[Add Members]
    
    UC5 --> UC5A[Import CSV]

2.2 User Stories
ID	User Story	Acceptance Criteria
US-1	As a user, I want to add contacts	Can enter name, birth date, gender and save
US-2	As a user, I want to create events linked to contacts	Can select person, event type, date, and reminder settings
US-3	As a user, I want automatic reminders	App shows notifications X days before events
US-4	As a user, I want to organize contacts into groups	Can create groups and assign multiple contacts
US-5	As a user, I want to import contacts from CSV	Can bulk import with field mapping
3. SYSTEM ARCHITECTURE
3.1 Three-Layer Architecture

text
graph TB
    subgraph Presentation["📱 PRESENTATION LAYER"]
        UI1[Main Window]
        UI2[Dashboard Screen]
        UI3[Persons Screen]
        UI4[Events Screen]
        UI5[Groups Screen]
        UI6[Reminder Window]
    end
    
    subgraph Business["⚙️ BUSINESS LOGIC LAYER"]
        SVC1[Notification Service]
        SVC2[Validation Logic]
        SVC3[Business Rules]
    end
    
    subgraph Data["💾 DATA ACCESS LAYER"]
        REPO1[Person Repository]
        REPO2[Event Repository]
        REPO3[Group Repository]
        REPO4[Database Deployer]
    end
    
    subgraph DB["🗄️ DATABASE LAYER"]
        SQL[(SQL Server Database)]
    end
    
    Presentation --> Business
    Business --> Data
    Data --> DB

3.2 Class Diagram (Core Components)

text
classDiagram
    class MainWindow {
        +show_screen()
        +navigate()
        +switch_theme()
    }
    
    class PersonRepository {
        +create(person)
        +read(id)
        +update(id, person)
        +delete(id)
        +get_all()
    }
    
    class EventRepository {
        +create(event)
        +get_upcoming(days)
        +get_by_person(person_id)
        +delete(id)
    }
    
    class NotificationService {
        +check_pending_reminders()
        +mark_as_sent(event_id)
        -calculate_reminder_date()
    }
    
    class DatabaseDeployer {
        +check_database_exists()
        +deploy_database()
        -execute_sql_script()
    }
    
    MainWindow --> PersonRepository
    MainWindow --> EventRepository
    NotificationService --> EventRepository
    PersonRepository --> Database
    EventRepository --> Database

3.3 Deployment Architecture

text
┌───────────────────────────────────┐
│    USER'S WINDOWS PC              │
│                                   │
│  ┌─────────────────────────────┐ │
│  │ Event_Reminder_System.exe   │ │
│  │  -  Python Runtime           │ │
│  │  -  CustomTkinter GUI        │ │
│  │  -  Business Logic           │ │
│  └──────────┬──────────────────┘ │
│             │ ODBC                │
│             │ TCP/IP :1433        │
│             ▼                     │
│  ┌─────────────────────────────┐ │
│  │ SQL Server (LocalDB/Express)│ │
│  │  -  Database Engine          │ │
│  │  -  Contact_Event_Reminder   │ │
│  └─────────────────────────────┘ │
│                                   │
│  config.json ← Configuration     │
└───────────────────────────────────┘

4. DATABASE DESIGN
4.1 Entity-Relationship Diagram

text
erDiagram
    PERSON ||--o{ EVENT : has
    PERSON ||--o{ PERSON_GROUP : belongs
    GROUP ||--o{ PERSON_GROUP : contains
    EVENT ||--|| EVENT_TYPE : categorized
    EVENT ||--o{ NOTIFICATION : triggers
    
    PERSON {
        int id PK
        nvarchar first_name
        nvarchar last_name
        date birth_date
        nvarchar gender
        bit is_active
        datetime2 created_at
    }
    
    EVENT {
        int id PK
        int person_id FK
        int event_type_id FK
        date event_date
        int reminder_days_before
        time reminder_time
        datetime2 created_at
    }
    
    EVENT_TYPE {
        int id PK
        nvarchar name UK
    }
    
    GROUP {
        int id PK
        nvarchar name
        datetime2 created_at
    }
    
    PERSON_GROUP {
        int person_id PK_FK
        int group_id PK_FK
        datetime2 added_at
    }
    
    NOTIFICATION {
        int id PK
        int event_id FK
        datetime2 sent_at
        nvarchar status
    }
    
    USER {
        int id PK
        nvarchar name
        nvarchar email UK
        bit notifications_enabled
        datetime2 created_at
    }

4.2 Database Schema
Table	Primary Key	Foreign Keys	Constraints
person	id	-	gender IN ('male','female','other')
event	id	person_id, event_type_id	reminder_days_before >= 0
event_type	id	-	name UNIQUE
group	id	-	-
person_group	person_id, group_id	person_id, group_id	CASCADE DELETE
notification	id	event_id	status IN ('planned','sent','failed')
user	id	-	email UNIQUE
4.3 Database Views
View Name	Purpose	Key Columns
v_upcoming_events	Shows future events with person details	event_id, person_name, event_date, days_until_event
v_event_summary	Categorizes events by time	event_id, person_name, time_category ('dnes', 'tento týden', etc.)
v_group_statistics	Group member and event counts	group_name, total_persons, total_events
4.4 Import/Export Schema

CSV Import Format:

text
first_name,last_name,birth_date,gender
Jan,Novák,1990-05-15,male
Marie,Svobodová,1985-12-20,female

Field	Type	Required	Format	Example
first_name	string	✅ Yes	-	Jan
last_name	string	✅ Yes	-	Novák
birth_date	date	❌ No	YYYY-MM-DD	1990-05-15
gender	string	❌ No	male/female/other	male
5. APPLICATION BEHAVIOR
5.1 Application State Diagram

text
stateDiagram-v2
    [*] --> Startup
    Startup --> CheckDB: Launch
    
    CheckDB --> ConfigDialog: DB Not Found
    CheckDB --> MainWindow: DB Exists
    
    ConfigDialog --> DeployDB: Save Config
    ConfigDialog --> [*]: Cancel
    
    DeployDB --> MainWindow: Success
    DeployDB --> Error: Failure
    
    MainWindow --> Dashboard: Navigate
    MainWindow --> Persons: Navigate
    MainWindow --> Events: Navigate
    MainWindow --> Groups: Navigate
    MainWindow --> Settings: Navigate
    
    Dashboard --> ReminderCheck: Every Hour
    ReminderCheck --> ReminderWindow: Events Found
    ReminderCheck --> Dashboard: No Events
    
    ReminderWindow --> Dashboard: Confirm/Postpone
    
    Error --> [*]: Exit

5.2 Reminder System Activity Diagram

text
flowchart TD
    Start([Application Starts]) --> Init[Initialize Services]
    Init --> Wait[Wait 1 Hour]
    Wait --> Check{Check Pending<br/>Reminders}
    
    Check -->|No Events| Wait
    Check -->|Events Found| Query[Query v_upcoming_events]
    
    Query --> Filter{Filter Events:<br/>days_until <= reminder_days}
    Filter -->|Matches Found| NotifCheck{Check if<br/>Already Sent Today}
    Filter -->|No Matches| Wait
    
    NotifCheck -->|Not Sent| Display[Display Reminder Window]
    NotifCheck -->|Already Sent| Wait
    
    Display --> UserAction{User Action}
    UserAction -->|Confirm| MarkSent[Mark as 'sent'<br/>in notification table]
    UserAction -->|Postpone| Close[Close Window]
    
    MarkSent --> Wait
    Close --> Wait

5.3 Key Workflows

Add New Event Workflow:

    User clicks "Události" → "+ Přidat"

    System loads persons and event types from DB

    User fills form (person, type, date, reminder_days)

    System validates inputs

    System executes INSERT with OUTPUT INSERTED.id

    System shows success message

    Table refreshes with new event

Reminder Check Workflow:

    Background thread sleeps 3600 seconds

    Wakes up and calls NotificationService.check_pending_reminders()

    Executes query on v_upcoming_events view

    Filters where days_until_event <= reminder_days_before

    Checks notification table for existing records today

    If new reminders exist, schedules ReminderNotificationWindow in main thread

    User acknowledges → INSERT into notification with status='sent'

6. CONFIGURATION
6.1 Configuration File: config.json

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

6.2 Configuration Options
Parameter	Type	Values	Description
server	string	., localhost, server\instance	SQL Server instance name
database	string	any valid DB name	Target database name
driver	string	ODBC Driver 17 for SQL Server	ODBC driver name
trusted_connection	boolean	true / false	Use Windows Authentication
default_reminder_days	integer	1-365	Default days before event to remind
6.3 Configuration Locations

    Development: Project root directory

    Production (EXE): Same directory as .exe file

    Auto-created: If missing, created with defaults on first run

7. INSTALLATION GUIDE
7.1 System Requirements
Component	Requirement
OS	Windows 10/11 (64-bit)
RAM	2 GB (4 GB recommended)
Disk Space	200 MB
SQL Server	SQL Server 2016+ or SQL Server Express (free)
ODBC Driver	ODBC Driver 17 for SQL Server
7.2 Installation Steps

STEP 1: Install SQL Server

text
1. Download SQL Server Express:
   https://www.microsoft.com/sql-server/sql-server-downloads
2. Run installer → Choose "Basic"
3. Note instance name (e.g., localhost\SQLEXPRESS)

STEP 2: Install ODBC Driver

text
1. Download ODBC Driver 17:
   https://go.microsoft.com/fwlink/?linkid=2249004
2. Run msodbcsql.msi
3. Complete installation

STEP 3: Run Application

text
1. Double-click Event_Reminder_System.exe
2. First launch: Configuration window appears
3. Enter SQL Server name (e.g., . or localhost\SQLEXPRESS)
4. Click "Otestovat připojení" (Test Connection)
5. Click "Uložit a pokračovat" (Save & Continue)
6. Database deploys automatically
7. Application starts

STEP 4: Verify Installation

text
1. Open SQL Server Management Studio (SSMS)
2. Connect to your server
3. Verify database "Contact_Event_Reminder_System" exists
4. Check tables: person, event, group, etc.

8. ERROR HANDLING
8.1 Common Errors
Error Code	Error Message	Cause	Solution
18456	Login failed for user	Authentication failure	Enable Windows Authentication in SQL Server
4060	Cannot open database	Database doesn't exist	Run database deployment from Settings
08001	Cannot connect to server	SQL Server not running	Start SQL Server service via services.msc
28000	SQL Server login error	Permissions issue	Verify user has db_owner role
42S02	Invalid object name (view)	Views not created	Reinitialize database from Settings
8.2 Error States

Application Launch Errors:

text
IF DB_NOT_FOUND:
    → Show DatabaseConfigWindow
    → User configures connection
    → Deploy database automatically
    
IF DB_CONNECTION_FAILED:
    → Show error dialog with details
    → Suggest checking SQL Server status
    → Allow manual configuration in Settings

Runtime Errors:

text
IF QUERY_FAILED:
    → Log error to console
    → Show user-friendly message
    → Continue application operation
    
IF REMINDER_CHECK_FAILED:
    → Log error
    → Skip this check cycle
    → Retry in next hour

8.3 Troubleshooting Guide

Problem: Application won't start

text
1. Check ODBC Driver is installed
2. Verify SQL Server is running (services.msc)
3. Review config.json for correct server name
4. Try running as Administrator

Problem: Reminders not showing

text
1. Verify event date is in future
2. Check reminder_days_before >= days_until_event
3. Look for existing notifications in database:
   SELECT * FROM notification WHERE event_id = X;
4. Delete test notifications if needed

9. THIRD-PARTY LIBRARIES
9.1 Python Dependencies
Library	Version	Purpose	License
customtkinter	5.2.2	Modern GUI framework	MIT
pyodbc	5.0.1	SQL Server database connectivity	MIT
Pillow	10.2.0	Image processing for GUI	HPND
python-dateutil	2.8.2	Date/time utilities	Apache 2.0
pyinstaller	6.3.0	Build tool for creating EXE	GPL
9.2 System Dependencies
Component	Version	Purpose
Python	3.10+	Runtime environment
ODBC Driver 17	Latest	SQL Server connectivity
SQL Server	2016+	Database engine
Windows SDK	-	System integration
9.3 License Compliance

All third-party libraries are open-source with permissive licenses (MIT, Apache 2.0) allowing educational and commercial use. This project complies with all license requirements.
10. PROJECT CONCLUSION
10.1 Achievements

✅ Fully Functional Desktop Application - Complete CRUD operations for contacts, events, and groups
✅ Automated Reminder System - Background service with hourly checks and popup notifications
✅ Professional Database Design - Normalized schema with 7 tables, 3 views, referential integrity
✅ User-Friendly Interface - Modern dark theme with intuitive navigation
✅ Robust Error Handling - Graceful degradation and informative error messages
✅ Import/Export Functionality - CSV import for bulk operations
✅ Auto-Deployment - Database automatically deploys on first run
10.2 Technical Highlights
Feature	Implementation
Architecture	Three-layer (Presentation, Business, Data Access)
Design Pattern	Repository Pattern for data access
Threading	Background daemon thread for reminders
GUI Framework	CustomTkinter with responsive screens
Database	SQL Server with views, triggers, and constraints
Deployment	Single EXE file with embedded Python runtime
10.3 Learning Outcomes

This project demonstrated proficiency in:

    Database Design: E-R modeling, normalization, views, stored procedures

    Software Engineering: Layered architecture, separation of concerns, modularity

    Python Development: GUI programming, threading, database connectivity

    SQL Server: T-SQL, ODBC, Windows Authentication

    User Experience: Intuitive workflows, error handling, configuration management

10.4 Future Enhancements

🔮 Potential Improvements:

    Email/SMS notifications via external API

    Cloud synchronization with Azure SQL

    Mobile companion app (React Native)

    Advanced reporting with charts (matplotlib)

    Recurring events (daily, weekly, monthly)

    Multi-user support with authentication

10.5 Statistics

text
Project Metrics:
├── Lines of Code: ~3,500
├── Python Files: 25
├── Database Tables: 7
├── Database Views: 3
├── Features Implemented: 15
├── Development Time: [X weeks]
└── Final EXE Size: ~65 MB

📄 APPENDICES
A. Project Structure

text
Event_Reminder_System/
├── main.py                          # Entry point
├── config.py                        # Configuration manager
├── requirements.txt                 # Dependencies
├── README.txt                       # Installation guide
├── database_export.sql              # DB deployment script
├── DOCUMENTATION.md                 # This file
│
├── ui/                              # Presentation layer
│   ├── main_window.py
│   ├── dashboard_screen.py
│   ├── persons_screen.py
│   ├── events_screen.py
│   ├── groups_screen.py
│   ├── settings_screen.py
│   └── reminder_notification_window.py
│
├── repositories/                    # Data access layer
│   ├── person_repository.py
│   ├── event_repository.py
│   ├── group_repository.py
│   ├── event_type_repository.py
│   └── database_deployer.py
│
├── services/                        # Business logic layer
│   └── notification_service.py
│
└── dist/                           # Build output
    └── Event_Reminder_System.exe

B. SQL Server Setup Commands

sql
-- Check SQL Server version
SELECT @@VERSION;

-- Check databases
SELECT name FROM sys.databases;

-- Check if application DB exists
SELECT database_id FROM sys.databases 
WHERE name = 'Contact_Event_Reminder_System';

-- Grant permissions to user
USE Contact_Event_Reminder_System;
ALTER ROLE db_owner ADD MEMBER [YourWindowsUser];

C. Build Commands

bash
# Install dependencies
pip install -r requirements.txt

# Run from source
python main.py

# Build EXE
pyinstaller --onefile --windowed --name="Event_Reminder_System" main.py

# Output: dist/Event_Reminder_System.exe

📞 CONTACT & SUPPORT

Author: [TVOJE JMÉNO]
Email: [TVŮJ EMAIL]
School: [NÁZEV ŠKOLY]
Date: 11.01.2026
Version: 1.0

© 2026 - Školní projekt vytvořený pro vzdělávací účely