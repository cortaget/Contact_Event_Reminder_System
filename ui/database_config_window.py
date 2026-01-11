import customtkinter as ctk
from config import Config
import pyodbc


class DatabaseConfigWindow(ctk.CTkToplevel):
    """Окно для ввода настроек подключения к БД"""

    def __init__(self, parent):
        super().__init__(parent)

        self.config = Config()
        self.success = False  # Флаг успешной настройки

        self.title("⚙️ Konfigurace databáze")
        self.geometry("1000x850")
        self.resizable(False, False)

        # Центрирование окна
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.winfo_screenheight() // 2) - (850 // 2)
        self.geometry(f"1000x850+{x}+{y}")

        # Блокировать закрытие крестиком
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

        # Поверх всех окон
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

        # Основная форма
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)

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
            placeholder_text="např. localhost\\SQLEXPRESS nebo ."
        )
        self.server_entry.pack(fill="x", pady=(0, 5))
        self.server_entry.insert(0, self.config.server)

        ctk.CTkLabel(
            form_frame,
            text="Příklady: . nebo localhost nebo localhost\\SQLEXPRESS",
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

        # Windows Authentication
        self.trusted_connection_var = ctk.BooleanVar(value=self.config.trusted_connection)

        self.trusted_connection_checkbox = ctk.CTkCheckBox(
            form_frame,
            text="Použít Windows Authentication (doporučeno)",
            variable=self.trusted_connection_var,
            font=ctk.CTkFont(size=13),
            checkbox_width=24,
            checkbox_height=24
        )
        self.trusted_connection_checkbox.pack(fill="x", pady=(10, 20))

        # Статус
        self.status_label = ctk.CTkLabel(
            form_frame,
            text="",
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        self.status_label.pack(fill="x", pady=(0, 10))

        # Кнопки
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 0))

        # Тест подключения
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

        # Сохранить и продолжить
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

        # Отмена
        self.cancel_button = ctk.CTkButton(
            button_frame,
            text="❌ Zrušit a ukončit",
            command=self.on_cancel,
            height=40,
            font=ctk.CTkFont(size=13),
            fg_color="gray40",
            hover_color="gray30"
        )
        self.cancel_button.pack(fill="x")

    def test_connection(self):
        """Проверить подключение к SQL Server"""
        self.status_label.configure(text="🔍 Testování připojení...", text_color="yellow")
        self.update()

        server = self.server_entry.get().strip()
        database = "master"  # Тестируем подключение к master
        driver = self.driver_entry.get().strip()
        trusted = self.trusted_connection_var.get()

        if not server or not driver:
            self.status_label.configure(
                text="❌ Vyplňte všechna pole!",
                text_color="red"
            )
            return

        try:
            # Попытка подключения
            conn_str = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};'
            if trusted:
                conn_str += 'Trusted_Connection=yes;'

            conn = pyodbc.connect(conn_str, timeout=10)
            conn.close()

            self.status_label.configure(
                text="✅ Připojení úspěšné! SQL Server je dostupný.",
                text_color="green"
            )

        except pyodbc.Error as e:
            error_msg = str(e)
            if "28000" in error_msg or "18456" in error_msg:
                self.status_label.configure(
                    text="❌ Chyba autentizace. Zkontrolujte Windows Authentication.",
                    text_color="red"
                )
            elif "08001" in error_msg:
                self.status_label.configure(
                    text="❌ Nelze se připojit k serveru. Zkontrolujte název serveru.",
                    text_color="red"
                )
            else:
                self.status_label.configure(
                    text=f"❌ Chyba: {error_msg[:60]}...",
                    text_color="red"
                )
        except Exception as e:
            self.status_label.configure(
                text=f"❌ Neočekávaná chyba: {str(e)[:60]}...",
                text_color="red"
            )

    def save_and_continue(self):
        """Сохранить настройки и продолжить"""
        server = self.server_entry.get().strip()
        database = self.database_entry.get().strip()
        driver = self.driver_entry.get().strip()
        trusted = self.trusted_connection_var.get()

        if not server or not database or not driver:
            self.status_label.configure(
                text="❌ Vyplňte všechna pole!",
                text_color="red"
            )
            return

        # Обновить config
        self.config.server = server
        self.config.database = database
        self.config.driver = driver
        self.config.trusted_connection = trusted

        # Сохранить в файл
        try:
            self.config.save()
            self.status_label.configure(
                text="✅ Konfigurace uložena!",
                text_color="green"
            )

            self.success = True
            self.after(500, self.destroy)  # Закрыть окно через 0.5 сек

        except Exception as e:
            self.status_label.configure(
                text=f"❌ Chyba ukládání: {str(e)[:60]}...",
                text_color="red"
            )

    def on_cancel(self):
        """Отмена - закрыть приложение"""
        if ctk.messagebox.askyesno(
                "Ukončit aplikaci",
                "Opravdu chcete ukončit aplikaci bez nastavení databáze?",
                icon="warning"
        ):
            self.success = False
            self.destroy()
