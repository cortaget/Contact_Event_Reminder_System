import customtkinter as ctk
from ui.screens.base_screen import BaseScreen
from config import Config
import pyodbc


class SettingsScreen(BaseScreen):
    def __init__(self, parent):
        super().__init__(parent)
        self.config = Config()

        # Заголовок
        title = ctk.CTkLabel(
            self,
            text="⚙ Nastavení",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Главный контейнер
        main_frame = ctk.CTkScrollableFrame(self)
        main_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)

        # === БЛОК 1: Připojení k databázi ===
        db_frame = ctk.CTkFrame(main_frame)
        db_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            db_frame,
            text="🗄️ Připojení k databázi",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 10), sticky="w")

        # Server
        ctk.CTkLabel(db_frame, text="Server:", anchor="w").grid(
            row=1, column=0, padx=15, pady=5, sticky="w"
        )
        self.server_entry = ctk.CTkEntry(db_frame, width=400)
        self.server_entry.insert(0, self.config.server)
        self.server_entry.grid(row=1, column=1, padx=15, pady=5, sticky="w")

        # Database
        ctk.CTkLabel(db_frame, text="Databáze:", anchor="w").grid(
            row=2, column=0, padx=15, pady=5, sticky="w"
        )
        self.database_entry = ctk.CTkEntry(db_frame, width=400)
        self.database_entry.insert(0, self.config.database)
        self.database_entry.grid(row=2, column=1, padx=15, pady=5, sticky="w")

        # Driver
        ctk.CTkLabel(db_frame, text="ODBC Driver:", anchor="w").grid(
            row=3, column=0, padx=15, pady=5, sticky="w"
        )
        self.driver_entry = ctk.CTkEntry(db_frame, width=400)
        self.driver_entry.insert(0, self.config.driver)
        self.driver_entry.grid(row=3, column=1, padx=15, pady=5, sticky="w")

        # Trusted Connection
        self.trusted_var = ctk.BooleanVar(value=self.config.trusted_connection)
        self.trusted_checkbox = ctk.CTkCheckBox(
            db_frame,
            text="Windows Authentication (Trusted Connection)",
            variable=self.trusted_var
        )
        self.trusted_checkbox.grid(row=4, column=0, columnspan=2, padx=15, pady=10, sticky="w")

        # Кнопки подключения
        btn_frame_db = ctk.CTkFrame(db_frame, fg_color="transparent")
        btn_frame_db.grid(row=5, column=0, columnspan=2, padx=15, pady=(10, 15), sticky="w")

        ctk.CTkButton(
            btn_frame_db,
            text="🔍 Otestovat připojení",
            command=self.test_connection,
            width=180
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame_db,
            text="💾 Uložit připojení",
            command=self.save_db_settings,
            width=150,
            fg_color="green"
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame_db,
            text="🔄 Inicializovat databázi",
            command=self.initialize_database,
            width=180,
            fg_color="#2B5278",
            hover_color="#1E3A5F"
        ).pack(side="left", padx=5)

        # === БЛОК 2: Nastavení upozornění ===
        notif_frame = ctk.CTkFrame(main_frame)
        notif_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            notif_frame,
            text="🔔 Nastavení upozornění",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 10), sticky="w")

        # Výchozí počet dní pro připomenutí
        ctk.CTkLabel(notif_frame, text="Výchozí připomenutí (dní):", anchor="w").grid(
            row=1, column=0, padx=15, pady=5, sticky="w"
        )
        self.reminder_days_entry = ctk.CTkEntry(notif_frame, width=100)
        self.reminder_days_entry.insert(0, str(self.config.default_reminder_days))
        self.reminder_days_entry.grid(row=1, column=1, padx=15, pady=5, sticky="w")

        # Povolit upozornění
        self.enable_notifications_var = ctk.BooleanVar(value=True)
        self.enable_notifications_checkbox = ctk.CTkCheckBox(
            notif_frame,
            text="Povolit automatická upozornění",
            variable=self.enable_notifications_var
        )
        self.enable_notifications_checkbox.grid(row=2, column=0, columnspan=2, padx=15, pady=10, sticky="w")

        # Кнопка сохранения
        ctk.CTkButton(
            notif_frame,
            text="💾 Uložit nastavení",
            command=self.save_notification_settings,
            width=150,
            fg_color="green"
        ).grid(row=3, column=0, columnspan=2, padx=15, pady=(10, 15), sticky="w")

        # === БЛОК 3: O aplikaci ===
        about_frame = ctk.CTkFrame(main_frame)
        about_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            about_frame,
            text="ℹ️ O aplikaci",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))

        ctk.CTkLabel(
            about_frame,
            text="📅 Personal Contacts & Events Manager\nVerze: 1.0.0\nAutor: Maxim\nRok: 2025",
            anchor="w",
            justify="left"
        ).pack(anchor="w", padx=15, pady=(0, 15))

    def test_connection(self):
        """Тестировать подключение к БД"""
        server = self.server_entry.get().strip()
        database = self.database_entry.get().strip()
        driver = self.driver_entry.get().strip()
        trusted = self.trusted_var.get()

        if not server or not database or not driver:
            self.show_message("Chyba", "Vyplňte všechna pole!", success=False)
            return

        # Формирование строки подключения
        conn_str = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};'
        if trusted:
            conn_str += 'Trusted_Connection=yes;'

        try:
            conn = pyodbc.connect(conn_str, timeout=5)
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            conn.close()

            self.show_message(
                "Úspěch",
                f"✅ Připojení úspěšné!\n\nSQL Server verze:\n{version[:100]}...",
                success=True
            )
        except Exception as e:
            self.show_message("Chyba", f"❌ Připojení selhalo:\n\n{str(e)}", success=False)

    def save_db_settings(self):
        """Сохранить настройки БД"""
        self.config.server = self.server_entry.get().strip()
        self.config.database = self.database_entry.get().strip()
        self.config.driver = self.driver_entry.get().strip()
        self.config.trusted_connection = self.trusted_var.get()

        try:
            self.config.save()
            self.show_message("Úspěch",
                              "✅ Nastavení připojení bylo uloženo!\n\nRestartujte aplikaci pro použití nových nastavení.",
                              success=True)
        except Exception as e:
            self.show_message("Chyba", f"❌ Chyba při ukládání:\n{str(e)}", success=False)

    def save_notification_settings(self):
        """Сохранить настройки уведомлений"""
        try:
            reminder_days = int(self.reminder_days_entry.get().strip())
            if reminder_days < 0:
                raise ValueError("Počet dní musí být kladný")

            self.config.default_reminder_days = reminder_days
            self.config.save()

            self.show_message("Úspěch", "✅ Nastavení upozornění bylo uloženo!", success=True)
        except ValueError as e:
            self.show_message("Chyba", f"❌ Neplatná hodnota:\n{str(e)}", success=False)

    def show_message(self, title, message, success=False):
        """Показать сообщение"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("500x250")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=450,
            justify="left"
        ).pack(padx=20, pady=30)

        ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            width=100
        ).pack(pady=10)

    def initialize_database(self):
        """Inicializovat databázi"""
        # Import zde pro vyhnuti se circular import
        from ui.database_setup_window import DatabaseSetupWindow

        # Dialog potvrzení
        dialog = ctk.CTkToplevel(self)
        dialog.title("Potvrzení")
        dialog.geometry("500x280")
        dialog.resizable(False, False)

        # Centrovani
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (280 // 2)
        dialog.geometry(f"500x280+{x}+{y}")

        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        # Nadpis
        ctk.CTkLabel(
            dialog,
            text="🔄 Inicializace databáze",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(padx=30, pady=(30, 15))

        # Text
        ctk.CTkLabel(
            dialog,
            text="Chcete spustit inicializaci databáze?\n\n"
                 "Vytvoří se nová databáze nebo se aktualizuje\n"
                 "struktura stávající databáze.\n\n"
                 "Existující data NEBUDOU smazána.",
            justify="center",
            font=ctk.CTkFont(size=13)
        ).pack(padx=30, pady=(0, 20))

        # Tlacitka
        def on_confirm():
            dialog.destroy()
            # Ulozit nastaveni pred inicializaci
            self.save_db_settings_silent()

            # Spustit okno inicializace
            setup_window = DatabaseSetupWindow(parent=self.winfo_toplevel())
            setup_window.run_initialization()

            # Po zavření zkontrolovat úspěch
            self.after(100, lambda: self.check_init_result(setup_window))

        def on_cancel():
            dialog.destroy()

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=(0, 30))

        ctk.CTkButton(
            btn_frame,
            text="❌ Zrušit",
            command=on_cancel,
            width=120,
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color="gray50",
            hover_color="gray40"
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="✅ Spustit",
            command=on_confirm,
            width=120,
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color="green",
            hover_color="darkgreen"
        ).pack(side="left", padx=10)

    def save_db_settings_silent(self):
        """Сохранить настройки БД без сообщения"""
        self.config.server = self.server_entry.get().strip()
        self.config.database = self.database_entry.get().strip()
        self.config.driver = self.driver_entry.get().strip()
        self.config.trusted_connection = self.trusted_var.get()
        try:
            self.config.save()
        except:
            pass

    def check_init_result(self, setup_window):
        """Zkontrolovat výsledek inicializace"""
        if setup_window.winfo_exists():
            # Okno stále existuje, zkontrolovat později
            self.after(100, lambda: self.check_init_result(setup_window))
        else:
            # Okno zavřeno, zkontrolovat úspěch
            if hasattr(setup_window, 'success') and setup_window.success:
                self.show_message(
                    "Úspěch",
                    "✅ Databáze byla úspěšně inicializována!",
                    success=True
                )
