USER DOCUMENTATION - Event Reminder System

Version: 1.0
Last Updated: January 5, 2026
Table of Contents

    Introduction

    System Requirements

    Installation

    First Launch

    Main Features

    How to Use

    Configuration

    Reminder System

    Troubleshooting

    FAQ

1. Introduction

Event Reminder System is a personal contacts and events management application designed to help you track important dates like birthdays, anniversaries, and other events. The application features an automatic reminder system that notifies you in advance of upcoming events.
Key Features:

    Contact Management - Store personal information about people

    Event Tracking - Track birthdays, anniversaries, and custom events

    Group Organization - Organize contacts into groups (family, friends, work)

    Automatic Reminders - Background notification system checks every hour

    Flexible Configuration - Customize database connection and reminder settings

    Reports - Generate statistics and upcoming events reports

2. System Requirements
Minimum Requirements:

    Operating System: Windows 10/11 (64-bit)

    RAM: 2 GB

    Disk Space: 200 MB free space

    Database: Microsoft SQL Server 2016+ or SQL Server Express

    ODBC Driver: ODBC Driver 17 for SQL Server

Recommended:

    RAM: 4 GB or more

    SQL Server: SQL Server 2019 or newer

3. Installation
Step 1: Install SQL Server

If you don't have SQL Server installed:

    Download SQL Server Express (free) from Microsoft website

    Install with default settings

    Remember your server name (usually localhost\SQLEXPRESS or .)

Step 2: Install ODBC Driver

    Download ODBC Driver 17 for SQL Server from:

        https://go.microsoft.com/fwlink/?linkid=2249004

    Run installer and complete installation

Step 3: Install Application

    Download Event_Reminder_System.exe

    Place it in any folder (e.g., C:\Program Files\EventReminder\)

    Double-click to launch

4. First Launch
Automatic Database Setup

When you launch the application for the first time, it will automatically detect that the database doesn't exist and show a setup wizard.

Setup Process:

    A dialog appears: "Database not found"

    Click "Create Database" (green button)

    The initialization window appears showing progress

    Wait for completion (usually 10-30 seconds)

    Click "Close" when done

The system will automatically create:

    Database structure (7 tables)

    Views for reports (3 views)

    Foreign key relationships

    Default settings

5. Main Features
5.1 Dashboard

The main screen shows:

    Upcoming Events - Next 30 days

    Statistics - Total contacts, events, groups

    Quick Actions - Add person, add event buttons

5.2 Contact Management (Osoby)

    Add new contacts with personal information

    Edit existing contacts

    Delete contacts (removes all associated events)

    Search and filter contacts

    View contact details

5.3 Events (Události)

    Create events linked to contacts

    Set event date and reminder preferences

    Choose event types (birthday, anniversary, custom)

    Edit or delete events

    Filter events (All, 30 days, 90 days)

5.4 Groups (Skupiny)

    Create groups (Family, Friends, Work, etc.)

    Add contacts to groups

    View group statistics

    Organize contacts by categories

5.5 Reminders (Upozornění)

Background system that:

    Checks for upcoming events every hour

    Shows popup notification window

    Displays events requiring attention

    Marks notifications as sent after confirmation

5.6 Reports (Reporty)

Generate reports:

    Upcoming events list

    Events by group

    Statistics summary

5.7 Import

    Import contacts from CSV files

    Bulk data upload

    Map CSV columns to database fields

5.8 Settings (Nastavení)

    Database connection configuration

    Default reminder days setting

    Test database connection

    Reinitialize database structure

6. How to Use
6.1 Adding a Contact

    Click "Osoby" (Contacts) in left menu

    Click "+ Přidat" (Add) button

    Fill in the form:

        First Name (required)

        Last Name (required)

        Birth Date (optional)

        Gender (optional)

    Click "Uložit" (Save)

6.2 Creating an Event

    Click "Události" (Events) in left menu

    Click "+ Přidat" (Add) button

    Fill in the form:

        Person - Select from dropdown

        Event Type - Select (Birthday, Anniversary, etc.)

        Event Date - Choose date

        Remind Days Before - How many days before to remind (default: 7)

        Reminder Time - What time to remind (default: 09:00)

    Click "Uložit" (Save)

6.3 Creating a Group

    Click "Skupiny" (Groups) in left menu

    Click "+ Přidat" (Add) button

    Enter Group Name

    Click "Uložit" (Save)

    To add members:

        Select the group

        Click "Přidat členy" (Add Members)

        Select contacts from list

        Click "Přidat vybrané" (Add Selected)

6.4 Editing Records

    Navigate to the section (Contacts, Events, or Groups)

    Select the row by clicking on it

    Click "Upravit" (Edit) button

    Modify the information

    Click "Uložit" (Save)

6.5 Deleting Records

    Navigate to the section

    Select the row

    Click "Smazat" (Delete) button (red)

    Confirm deletion

⚠️ Warning: Deleting a contact will also delete all their events!
7. Configuration
7.1 Configuration File (config.json)

The application stores settings in config.json located in the same folder as the EXE file.

Default Configuration:

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

7.2 Changing Database Settings

Method 1: Via Settings Menu

    Click "Nastavení" (Settings) in left menu

    Enter new values:

        Server - SQL Server instance name

        Database - Database name

        Driver - ODBC driver name

    Check "Use Windows Authentication" if applicable

    Click "Test Connection" to verify

    Click "Save" if test succeeds

Method 2: Edit config.json Manually

    Close the application

    Open config.json in text editor (Notepad)

    Modify values:

        "server": "localhost\\SQLEXPRESS" - Your SQL Server name

        "database": "YourDatabaseName" - Database name

    Save file

    Restart application

7.3 Common Server Names

    Local SQL Express: localhost\SQLEXPRESS or .\SQLEXPRESS

    Local SQL Server: localhost or .

    Remote Server: 192.168.1.100 or ServerName

    Named Instance: ServerName\InstanceName

8. Reminder System
8.1 How It Works

The reminder system operates in two modes:

1. Startup Check

    When you launch the application

    Checks for pending reminders after 2 seconds

    Shows notification window if events require attention

2. Background Checking

    Runs in background thread

    Checks every 1 hour (3600 seconds)

    Automatically displays notifications

8.2 Reminder Logic

A reminder is triggered when:

    Event date is today or in the future

    Days until event ≤ Reminder days before setting

    Notification hasn't been sent today

Example:

    Event date: January 10, 2026

    Today: January 5, 2026

    Reminder days before: 7

    Days until event: 5

    Result: ✅ Reminder shown (5 ≤ 7)

8.3 Notification Window

When reminders are triggered, a popup window appears showing:

    Event cards with color-coded urgency:

        🎉 Red - Event is TODAY

        ⏰ Orange - Event is TOMORROW

        📅 Blue - Event in 3-7 days

        📆 Gray - Event in 8+ days

    Person name and event type

    Event date and days remaining

Actions:

    "Confirm and Close" (green) - Mark all as read, won't show again today

    "Remind Later" (gray) - Close window, will show again in 1 hour

8.4 Testing Reminders

To test the reminder system:

    Create an event with date tomorrow

    Set "Remind days before" to 7 or more

    Wait 2 seconds after startup - notification should appear

    Or wait 1 hour - background check will trigger

9. Troubleshooting
Problem: Application won't start

Possible Causes:

    Missing ODBC Driver

    SQL Server not running

    Incorrect database configuration

Solutions:

    Install ODBC Driver 17 for SQL Server

    Start SQL Server service:

        Press Win + R

        Type services.msc

        Find SQL Server (SQLEXPRESS)

        Right-click → Start

    Check config.json settings

Problem: "Database not found" error

Solution:
Click "Create Database" in the setup dialog. The application will automatically create the database structure.
Problem: "Connection failed" in Settings

Possible Causes:

    Wrong server name

    SQL Server not running

    Windows Authentication disabled

Solutions:

    Verify SQL Server is running

    Test server name:

        Open Command Prompt

        Type: sqlcmd -S localhost\SQLEXPRESS -E

        If connects successfully, server name is correct

    Ensure Windows Authentication is enabled

Problem: Reminders not showing

Possible Causes:

    Event date is too far in future

    Event is in the past

    Reminder already sent today

Solutions:

    Check event date is within reminder range:

        Go to Události (Events)

        Verify Event Date and Remind Days Before

    Ensure event date ≥ today

    Check notification table in database:

sql
SELECT * FROM notification;

Delete test notifications if needed:

    sql
    DELETE FROM notification WHERE event_id = [your_event_id];

Problem: "config.json" not found

Solution:
The application creates config.json automatically on first run. If deleted:

    Run the application

    It will recreate with default settings

    Modify settings via Settings menu

10. FAQ
Q: Can I use a remote SQL Server?

A: Yes! In Settings, change the Server to your remote server address (e.g., 192.168.1.100 or server.domain.com). Ensure SQL Server allows remote connections and firewall permits port 1433.
Q: How do I backup my data?

A: Backup the SQL Server database:

    Open SQL Server Management Studio

    Right-click your database → Tasks → Back Up

    Choose backup location

    Click OK

Q: Can I change the reminder check frequency?

A: Currently set to 1 hour. To modify, you need to edit main.py and change time.sleep(3600) to desired seconds, then rebuild the EXE.
Q: What happens if I delete a contact?

A: All events associated with that contact are also deleted due to CASCADE DELETE relationship. Always backup before mass deletions.
Q: Can I import existing contacts?

A: Yes! Use the Import feature:

    Prepare CSV file with columns: first_name, last_name, birth_date

    Click Import in menu

    Select your CSV file

    Map columns

    Click Import

Q: How do I run on another computer?

A: Copy these files:

    Event_Reminder_System.exe

    config.json (optional - will be created automatically)

On the new computer:

    Install SQL Server (if needed)

    Install ODBC Driver 17

    Run the EXE

    Configure database connection in Settings

Q: Is my data secure?

A: Data is stored locally in your SQL Server database. The application uses Windows Authentication by default, which is secure. For remote access, use SQL Server authentication with strong passwords.