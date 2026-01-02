import customtkinter as ctk
from ui.screens.dashboard_screen import DashboardScreen
from ui.screens.persons_screen import PersonsScreen
from ui.screens.events_screen import EventsScreen
from ui.screens.groups_screen import GroupsScreen
from ui.screens.notifications_screen import NotificationsScreen
from ui.screens.reports_screen import ReportsScreen
from ui.screens.import_screen import ImportScreen
from ui.screens.settings_screen import SettingsScreen


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Настройки окна
        self.title("Personal Contacts & Events Manager")
        self.geometry("1200x700")

        # Тема
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Основной layout: sidebar + content
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Боковая панель навигации
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)

        # Лого
        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="📅 Event Manager",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Кнопки навигации
        self.nav_buttons = {}
        nav_items = [
            ("🏠 Dashboard", "dashboard"),
            ("🧍 Osoby", "persons"),
            ("🎉 Události", "events"),
            ("👥 Skupiny", "groups"),
            ("🔔 Upozornění", "notifications"),
            ("📊 Reporty", "reports"),
            ("📥 Import", "import"),
            ("⚙ Nastavení", "settings")
        ]

        for idx, (text, screen_name) in enumerate(nav_items):
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=lambda s=screen_name: self.show_screen(s),
                anchor="w",
                height=40
            )
            btn.grid(row=idx + 1, column=0, padx=10, pady=5, sticky="ew")
            self.nav_buttons[screen_name] = btn

        # Контейнер для экранов
        self.content_frame = ctk.CTkFrame(self, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Инициализация всех экранов
        self.screens = {
            "dashboard": DashboardScreen(self.content_frame),
            "persons": PersonsScreen(self.content_frame),
            "events": EventsScreen(self.content_frame),
            "groups": GroupsScreen(self.content_frame),
            "notifications": NotificationsScreen(self.content_frame),
            "reports": ReportsScreen(self.content_frame),
            "import": ImportScreen(self.content_frame),
            "settings": SettingsScreen(self.content_frame)
        }

        # Показать dashboard по умолчанию
        self.current_screen = None
        self.show_screen("dashboard")

    def show_screen(self, screen_name):
        """Переключение между экранами"""
        if self.current_screen:
            self.screens[self.current_screen].hide()

        self.screens[screen_name].show()
        self.current_screen = screen_name

        # Подсветка активной кнопки
        for name, btn in self.nav_buttons.items():
            if name == screen_name:
                btn.configure(fg_color=("gray75", "gray25"))
            else:
                btn.configure(fg_color=("gray85", "gray15"))
