import customtkinter as ctk
from config import Config
import pyodbc


class DatabaseConfigWindow(ctk.CTkToplevel):
    """Окно для ввода настроек подключения к БД"""

    def __init__(self, parent):
        super().__init__(parent)

        self.config = Config()
        self.success = False

        self.title("⚙️ Konfigurace databáze")
        self.geometry("700x950")
        self.resizable(False, False)

        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.winfo_screenheight() // 2) - (950 // 2)
        self.geometry(f"700x950+{x}+{y}")

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.attributes('-topmost', True)
        self.lift()
        self.focus_force()

        self.create_widgets()

    def create_widgets(self):
        """Создать интерфейс"""

        # Заголовок
        header = ctk.CTkFrame(self, fg_color="#1f538d", height=100)
        header.pack(fill="x", padx=0, pady=0)

        ctk.CTkLabel(
            header,
            text="⚙️ Konfigurace databáze",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            header,
            text="Databáze nebyla nalezena. Zadejte připojovací údaje.",
            font=ctk.CTkFont(size=12),
            text_color="white"
        ).pack(pady=(0, 20))

        # Scrollable форма
        scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True, padx=30, pady=20)

        form_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True)

        # Server
        ctk.CTkLabel(
            form_frame,
            text="SQL Server:",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        ).pack(fill="x", pady=(10, 5))

        self.server_entry = ctk.CTkEntry(
            form_frame,
            height=35,
            font=ctk.CTkFont(size=13),
            placeholder_text="např. localhost nebo 192.168.1.50"
        )
        self.server_entry.pack(fill="x", pady=(0, 5))
        self.server_entry.insert(0, self.config.server)

        ctk.CTkLabel(
            form_frame,
            text="Příklady: localhost, 192.168.1.100, server.domain.com",
            font=ctk.CTkFont(size=10),
            text_color="gray",
            anchor="w"
        ).pack(fill="x", pady=(0, 10))

        # Database
        ctk.CTkLabel(
            form_frame,
            text="Název databáze:",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        ).pack(fill="x", pady=(10, 5))

        self.database_entry = ctk.CTkEntry(
            form_frame,
            height=35,
            font=ctk.CTkFont(size=13),
            placeholder_text="Contact_Event_Reminder_System"
        )
        self.database_entry.pack(fill="x", pady=(0, 15))
        self.database_entry.insert(0, self.config.database)

        # Driver
        ctk.CTkLabel(
            form_frame,
            text="ODBC Driver:",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        ).pack(fill="x", pady=(10, 5))

        self.driver_entry = ctk.CTkEntry(
            form_frame,
            height=35,
            font=ctk.CTkFont(size=13)
        )
        self.driver_entry.pack(fill="x", pady=(0, 15))
        self.driver_entry.insert(0, self.config.driver)

        # Separator
        separator = ctk.CTkFrame(form_frame, height=2, fg_color="gray30")
        separator.pack(fill="x", pady=20)

        ctk.CTkLabel(
            form_frame,
            text="Typ autentizace:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 10))

        # Windows Authentication checkbox
        self.trusted_connection_var = ctk.BooleanVar(value=self.config.trusted_connection)

        self.trusted_connection_checkbox = ctk.CTkCheckBox(
            form_frame,
            text="Windows Authentication (integrované ověření)",
            variable=self.trusted_connection_var,
            font=ctk.CTkFont(size=13),
            checkbox_width=24,
            checkbox_height=24,
            command=self.toggle_auth_mode
        )
        self.trusted_connection_checkbox.pack(fill="x", pady=(0, 15))

        # Username
        self.username_label = ctk.CTkLabel(
            form_frame,
            text="Uživatelské jméno (SQL Login):",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        self.username_label.pack(fill="x", pady=(10, 5))

        self.username_entry = ctk.CTkEntry(
            form_frame,
            height=35,
            font=ctk.CTkFont(size=13),
            placeholder_text="např. sa"
        )
        self.username_entry.pack(fill="x", pady=(0, 15))
        self.username_entry.insert(0, self.config.username)

        # Password
        self.password_label = ctk.CTkLabel(
            form_frame,
            text="Heslo:",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        self.password_label.pack(fill="x", pady=(10, 5))

        self.password_entry = ctk.CTkEntry(
            form_frame,
            height=35,
            font=ctk.CTkFont(size=13),
            placeholder_text="Zadejte heslo",
            show="●"
        )
        self.password_entry.pack(fill="x", pady=(0, 20))
        self.password_entry.insert(0, self.config.password)

        # Info label
        self.auth_info_label = ctk.CTkLabel(
            form_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="w",
            wraplength=620
        )
        self.auth_info_label.pack(fill="x", pady=(0, 10))

        # Применить начальное состояние
        self.toggle_auth_mode()

        # Статус
        self.status_label = ctk.CTkLabel(
            form_frame,
            text="",
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        self.status_label.pack(fill="x", pady=(10, 10))

        # Кнопки
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 0))

        self.test_button = ctk.CTkButton(
            button_frame,
            text="🔍 Otestovat připojení",
            command=self.test_connection,
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color="#3a7ebf",
            hover_color="#2d5f8f"
        )
        self.test_button.pack(fill="x", pady=(0, 10))

        self.save_button = ctk.CTkButton(
            button_frame,
            text="✅ Uložit a pokračovat",
            command=self.save_and_continue,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="green",
            hover_color="darkgreen"
        )
        self.save_button.pack(fill="x", pady=(0, 10))

        self.cancel_button = ctk.CTkButton(
            button_frame,
            text="❌ Zrušit a ukončit",
            command=self.on_cancel,
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color="gray40",
            hover_color="gray30"
        )
        self.cancel_button.pack(fill="x", pady=(0, 30))

    def toggle_auth_mode(self):
        """Переключить режим аутентификации"""
        if self.trusted_connection_var.get():
            self.username_entry.configure(state="disabled", fg_color="gray20")
            self.password_entry.configure(state="disabled", fg_color="gray20")
            self.username_label.configure(text_color="gray50")
            self.password_label.configure(text_color="gray50")
            self.auth_info_label.configure(
                text="ℹ️ Používá se Windows účet pro připojení k SQL Serveru.",
                text_color="gray"
            )
        else:
            self.username_entry.configure(state="normal", fg_color=["#F9F9FA", "#343638"])
            self.password_entry.configure(state="normal", fg_color=["#F9F9FA", "#343638"])
            self.username_label.configure(text_color="white")
            self.password_label.configure(text_color="white")
            self.auth_info_label.configure(
                text="ℹ️ Používá se SQL Server login. Ujistěte se, že Mixed Mode je povolen.",
                text_color="orange"
            )

    def test_connection(self):
        """Проверить подключение к SQL Server"""
        self.status_label.configure(text="🔍 Testování připojení...", text_color="yellow")
        self.update()

        server = self.server_entry.get().strip()
        database = "master"
        driver = self.driver_entry.get().strip()
        trusted = self.trusted_connection_var.get()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not server or not driver:
            self.status_label.configure(text="❌ Vyplňte server a driver!", text_color="red")
            return

        if not trusted and not username:
            self.status_label.configure(text="❌ Zadejte login nebo použijte Windows Auth!", text_color="red")
            return

        try:
            conn_str = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};'
            if trusted:
                conn_str += 'Trusted_Connection=yes;'
            else:
                conn_str += f'UID={username};PWD={password};'

            conn = pyodbc.connect(conn_str, timeout=10)
            conn.close()

            self.status_label.configure(text="✅ Připojení úspěšné!", text_color="green")

        except pyodbc.Error as e:
            error_msg = str(e)
            if "18456" in error_msg:
                self.status_label.configure(text="❌ Chybné přihlašovací údaje.", text_color="red")
            elif "08001" in error_msg:
                self.status_label.configure(text="❌ Nelze se připojit k serveru.", text_color="red")
            else:
                self.status_label.configure(text=f"❌ Chyba: {error_msg[:70]}...", text_color="red")
        except Exception as e:
            self.status_label.configure(text=f"❌ Chyba: {str(e)[:70]}...", text_color="red")

    def save_and_continue(self):
        """Сохранить настройки и продолжить"""
        server = self.server_entry.get().strip()
        database = self.database_entry.get().strip()
        driver = self.driver_entry.get().strip()
        trusted = self.trusted_connection_var.get()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not server or not database or not driver:
            self.status_label.configure(text="❌ Vyplňte povinná pole!", text_color="red")
            return

        if not trusted and not username:
            self.status_label.configure(text="❌ Zadejte login!", text_color="red")
            return

        self.config.server = server
        self.config.database = database
        self.config.driver = driver
        self.config.trusted_connection = trusted
        self.config.username = username
        self.config.password = password

        try:
            self.config.save()
            self.status_label.configure(text="✅ Uloženo!", text_color="green")
            self.success = True
            self.after(500, self.destroy)
        except Exception as e:
            self.status_label.configure(text=f"❌ Chyba: {str(e)[:70]}...", text_color="red")

    def on_cancel(self):
        """Отмена"""
        try:
            from tkinter import messagebox
            result = messagebox.askyesno(
                "Ukončit aplikaci",
                "Opravdu chcete ukončit bez nastavení databáze?",
                icon="warning"
            )
            if result:
                self.success = False
                self.destroy()
        except:
            self.success = False
            self.destroy()
