import customtkinter as ctk
from database_initializer import DatabaseInitializer
from config import Config
import sys
import threading


class TestDatabaseSetupWindow(ctk.CTk):
    """Window for test database creation with manual start button"""

    def __init__(self, test_db_name):
        super().__init__()

        self.test_db_name = test_db_name
        self.success = False
        self.initializer = DatabaseInitializer()

        # Window setup
        self.title(f"🧪 Test Database Creation: {self.test_db_name}")
        self.geometry("800x700")
        self.resizable(False, False)

        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.winfo_screenheight() // 2) - (700 // 2)
        self.geometry(f"800x700+{x}+{y}")

        # Block closing during creation
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.create_widgets()

    def create_widgets(self):
        """Create all widgets"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="🗄️ Database Initialization",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(padx=30, pady=(40, 15))

        # Database name info
        info_frame = ctk.CTkFrame(self, fg_color="gray25", corner_radius=12)
        info_frame.pack(padx=30, pady=15, fill="x")

        ctk.CTkLabel(
            info_frame,
            text=f"📦 Database to create: {self.test_db_name}",
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w"
        ).pack(anchor="w", padx=20, pady=15)

        # Description
        desc = ctk.CTkLabel(
            self,
            text="Click the button below to start database creation",
            font=ctk.CTkFont(size=15),
            text_color="gray"
        )
        desc.pack(padx=30, pady=(10, 25))

        # CREATE DATABASE BUTTON (BIG AND GREEN)
        self.create_button = ctk.CTkButton(
            self,
            text="🚀 CREATE DATABASE",
            command=self.start_creation,
            width=400,
            height=60,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="green",
            hover_color="darkgreen"
        )
        self.create_button.pack(padx=30, pady=20)

        # Log frame (hidden initially)
        self.log_frame = ctk.CTkScrollableFrame(self, height=300)
        self.log_frame.pack(padx=30, pady=15, fill="both", expand=True)
        self.log_frame.pack_forget()  # Hide initially

        # Progress bar (hidden initially)
        self.progress = ctk.CTkProgressBar(self, width=740, height=20)
        self.progress.pack(padx=30, pady=15)
        self.progress.set(0)
        self.progress.pack_forget()  # Hide initially

        # Status (hidden initially)
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(padx=30, pady=(0, 15))
        self.status_label.pack_forget()  # Hide initially

        # Close button
        self.close_button = ctk.CTkButton(
            self,
            text="Close",
            command=self.on_close,
            width=180,
            height=45,
            font=ctk.CTkFont(size=14)
        )
        self.close_button.pack(pady=(0, 30))

    def start_creation(self):
        """Start database creation process"""
        # Hide create button
        self.create_button.pack_forget()

        # Show log, progress, status
        self.log_frame.pack(padx=30, pady=15, fill="both", expand=True)
        self.progress.pack(padx=30, pady=15)
        self.progress.set(0)
        self.status_label.pack(padx=30, pady=(0, 15))

        # Disable close button
        self.close_button.configure(state="disabled", text="Creating...")

        # Start creation
        self.run_initialization()

    def add_log(self, message, color="white"):
        """Add message to log"""
        log_label = ctk.CTkLabel(
            self.log_frame,
            text=message,
            anchor="w",
            text_color=color,
            font=ctk.CTkFont(size=12)
        )
        log_label.pack(anchor="w", padx=10, pady=2, fill="x")
        self.log_frame._parent_canvas.yview_moveto(1.0)

    def update_status(self, message):
        """Update status"""
        self.status_label.configure(text=message)
        self.update()

    def update_progress(self, value):
        """Update progress bar (0.0 - 1.0)"""
        self.progress.set(value)
        self.update()

    def run_initialization(self):
        """Run database initialization"""
        # Change DB name in initializer
        self.initializer.config.database = self.test_db_name

        def init_thread():
            try:
                # Step 1: Check DB existence
                self.update_status("Checking database...")
                self.add_log("🔍 Checking if database exists...", "cyan")
                self.update_progress(0.1)

                db_exists = self.initializer.check_database_exists()

                if db_exists:
                    self.add_log("✅ Database already exists", "green")
                    self.update_progress(1.0)
                    self.update_status("Database ready!")
                    self.success = True
                    self.enable_close()
                    return

                self.add_log("⚠️ Database not found", "yellow")
                self.update_progress(0.2)

                # Step 2: Create DB
                self.update_status("Creating database...")
                self.add_log(f"🔨 Creating database [{self.initializer.config.database}]...", "cyan")
                self.update_progress(0.3)

                if not self.initializer.create_database():
                    self.add_log("❌ ERROR: Failed to create database!", "red")
                    self.add_log("", "white")
                    self.add_log("Possible causes:", "yellow")
                    self.add_log("  • SQL Server is not running", "white")
                    self.add_log("  • Invalid connection settings", "white")
                    self.add_log("  • No permission to create database", "white")
                    self.add_log("", "white")
                    self.add_log("Solution:", "yellow")
                    self.add_log("  1. Start SQL Server service", "white")
                    self.add_log("  2. Check settings in config.json", "white")
                    self.update_status("❌ Database creation failed")
                    self.update_progress(0)
                    self.enable_close()
                    return

                self.add_log(f"✅ Database [{self.initializer.config.database}] created!", "green")
                self.update_progress(0.5)

                # Step 3: Create structure
                self.update_status("Creating tables and views...")
                self.add_log("🔨 Creating database structure...", "cyan")
                self.update_progress(0.6)

                if not self.initializer.initialize_schema():
                    self.add_log("❌ ERROR: Failed to create database structure!", "red")
                    self.update_status("❌ Structure initialization failed")
                    self.update_progress(0)
                    self.enable_close()
                    return

                self.update_progress(0.75)
                self.add_log("✅ Table created: person", "green")
                self.add_log("✅ Table created: group", "green")
                self.add_log("✅ Table created: person_group", "green")
                self.add_log("✅ Table created: event_type", "green")
                self.add_log("✅ Table created: event", "green")
                self.add_log("✅ Table created: notification", "green")

                self.update_progress(0.9)
                self.add_log("✅ View created: v_upcoming_events", "green")
                self.add_log("✅ View created: v_event_summary", "green")
                self.add_log("✅ View created: v_group_statistics", "green")

                self.update_progress(1.0)
                self.add_log("", "white")
                self.add_log("=" * 60, "cyan")
                self.add_log("✅ DATABASE SUCCESSFULLY CONFIGURED!", "green")
                self.add_log("=" * 60, "cyan")

                self.update_status("✅ Complete!")
                self.success = True
                self.enable_close()

            except Exception as e:
                self.add_log(f"❌ CRITICAL ERROR: {e}", "red")
                import traceback
                error_details = traceback.format_exc()
                for line in error_details.split('\n'):
                    if line.strip():
                        self.add_log(f"  {line}", "red")
                self.update_status("❌ Critical error")
                self.update_progress(0)
                self.enable_close()

        # Run in separate thread
        thread = threading.Thread(target=init_thread, daemon=True)
        thread.start()

    def enable_close(self):
        """Enable close button"""
        self.close_button.configure(state="normal", text="Close")
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def on_close(self):
        """Handle window close"""
        if self.close_button.cget("state") == "normal":
            self.destroy()


def show_db_name_dialog():
    """Dialog for selecting test DB name"""
    root = ctk.CTk()
    root.withdraw()

    dialog = ctk.CTkToplevel(root)
    dialog.title("🧪 Test Mode - Database Setup")
    dialog.geometry("1000x1000")
    dialog.resizable(False, False)

    # Center window
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (700 // 2)
    y = (dialog.winfo_screenheight() // 2) - (480 // 2)
    dialog.geometry(f"1000x1000+{x}+{y}")

    result = [None]

    # Title
    ctk.CTkLabel(
        dialog,
        text="🧪 Test Database Creation",
        font=ctk.CTkFont(size=26, weight="bold")
    ).pack(padx=30, pady=(40, 15))

    # Subtitle
    ctk.CTkLabel(
        dialog,
        text="Create a separate test database without affecting your main data",
        font=ctk.CTkFont(size=14),
        text_color="gray"
    ).pack(padx=30, pady=(0, 25))

    # Current settings
    config = Config()

    info_frame = ctk.CTkFrame(dialog, fg_color="gray25", corner_radius=12)
    info_frame.pack(padx=30, pady=15, fill="x")

    ctk.CTkLabel(
        info_frame,
        text="📋 Current Connection Settings:",
        font=ctk.CTkFont(size=15, weight="bold"),
        anchor="w"
    ).pack(anchor="w", padx=20, pady=(15, 10))

    settings_text = f"""   Server: {config.server}
   Main Database: {config.database}
   Driver: {config.driver}"""

    ctk.CTkLabel(
        info_frame,
        text=settings_text,
        anchor="w",
        font=ctk.CTkFont(size=13),
        justify="left"
    ).pack(anchor="w", padx=20, pady=(0, 15))

    # Warning box
    warning_frame = ctk.CTkFrame(dialog, fg_color="#FF8C00", corner_radius=12)
    warning_frame.pack(padx=30, pady=20, fill="x")

    ctk.CTkLabel(
        warning_frame,
        text="⚠️ Your main database will NOT be affected!",
        font=ctk.CTkFont(size=15, weight="bold"),
        text_color="black"
    ).pack(padx=15, pady=12)

    # Test DB name input
    ctk.CTkLabel(
        dialog,
        text="Test Database Name:",
        anchor="w",
        font=ctk.CTkFont(size=14, weight="bold")
    ).pack(padx=30, pady=(15, 8), anchor="w")

    test_db_name = f"{config.database}_TEST"
    name_entry = ctk.CTkEntry(dialog, width=640, height=40, font=ctk.CTkFont(size=14))
    name_entry.insert(0, test_db_name)
    name_entry.pack(padx=30, pady=(0, 25))

    # Buttons
    def on_continue():
        name = name_entry.get().strip()
        if name:
            result[0] = name
            dialog.destroy()
            root.destroy()

    def on_cancel():
        dialog.destroy()
        root.destroy()

    btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
    btn_frame.pack(padx=30, pady=(0, 30))

    ctk.CTkButton(
        btn_frame,
        text="❌ Cancel",
        command=on_cancel,
        width=150,
        height=45,
        font=ctk.CTkFont(size=14),
        fg_color="gray50",
        hover_color="gray40"
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        btn_frame,
        text="✅ Continue",
        command=on_continue,
        width=200,
        height=45,
        font=ctk.CTkFont(size=14),
        fg_color="green",
        hover_color="darkgreen"
    ).pack(side="left", padx=10)

    dialog.wait_window()
    return result[0]


def main():
    """Main testing function"""
    try:
        # Setup appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Step 1: Show dialog to enter DB name
        print("🪟 Opening database setup window...")
        test_db_name = show_db_name_dialog()

        if not test_db_name:
            print("\n❌ Cancelled by user")
            return

        print(f"✅ Selected database name: {test_db_name}")

        # Step 2: Show window with CREATE BUTTON
        print(f"🪟 Opening creation window...\n")

        window = TestDatabaseSetupWindow(test_db_name)
        window.mainloop()

        # Step 3: Check result
        if window.success:
            print("\n✅ Test database successfully created!")
            print(f"   Name: {test_db_name}")

            # Offer to run application with test DB
            answer = input("\n💡 Launch application with test database? (y/n): ").lower()

            if answer == 'y':
                from ui.main_window import MainWindow

                # Temporarily change DB name in config
                config = Config()
                original_db = config.database
                config.database = test_db_name

                print(f"\n🚀 Launching with DB [{test_db_name}]...\n")

                # Run application
                app = MainWindow()
                app.mainloop()

                # Restore original name
                config.database = original_db
                print(f"\n✅ Restored to main DB: {original_db}")
        else:
            print("\n❌ Failed to create test database or cancelled")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
