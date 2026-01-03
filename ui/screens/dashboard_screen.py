import customtkinter as ctk
from ui.screens.base_screen import BaseScreen
from repositories.report_repository import ReportRepository


class DashboardScreen(BaseScreen):
    def __init__(self, parent):
        super().__init__(parent)
        self.report_repo = ReportRepository()

        # Заголовок
        title = ctk.CTkLabel(
            self,
            text="📅 Nadcházející události",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Таблица событий
        self.events_frame = ctk.CTkScrollableFrame(self, height=400)
        self.events_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)

        # Кнопки
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkButton(
            btn_frame,
            text="🔘 Zobrazit všechny události",
            command=self.show_all_events,
            height=40
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="➕ Přidat osobu",
            command=self.add_person,
            height=40
        ).pack(side="left", padx=5)

        # Загрузка данных
        self.load_upcoming_events()

    def load_upcoming_events(self):
        """Загрузить ближайшие события"""
        # Очистка
        for widget in self.events_frame.winfo_children():
            widget.destroy()

        # Заголовки колонок
        headers = ["Osoba", "Typ", "Datum", "Za dní"]
        for idx, header in enumerate(headers):
            label = ctk.CTkLabel(
                self.events_frame,
                text=header,
                font=ctk.CTkFont(weight="bold")
            )
            label.grid(row=0, column=idx, padx=10, pady=5, sticky="w")

        # Данные
        try:
            upcoming = self.report_repo.get_upcoming_events_report(30)

            # Словарь иконок для типов событий
            type_icons = {
                "birthday": "🎂",
                "anniversary": "💍",
                "other": "🎉"
            }

            for idx, event in enumerate(upcoming, start=1):
                # Получение типа события
                # Получаем тип события
                event_type = getattr(event, 'event_type', 'other')

                # Словарь иконок
                type_icons = {
                    "birthday": "🎂",
                    "anniversary": "💍",
                    "other": "🎉"
                }
                icon = type_icons.get(event_type, "🎉")

                first_name = getattr(event, 'first_name', 'N/A')
                last_name = getattr(event, 'last_name', '')
                event_date = getattr(event, 'event_date', 'N/A')

                # Колонка: Osoba
                ctk.CTkLabel(self.events_frame, text=f"{first_name} {last_name}").grid(
                    row=idx, column=0, padx=10, pady=2, sticky="w"
                )

                # Колонка: Typ
                ctk.CTkLabel(self.events_frame, text=f"{icon} {event_type}").grid(
                    row=idx, column=1, padx=10, pady=2, sticky="w"
                )

                # Колонка: Datum
                ctk.CTkLabel(self.events_frame, text=str(event_date)).grid(
                    row=idx, column=2, padx=10, pady=2, sticky="w"
                )

                # Колонка: Za dní (расчёт)
                try:
                    from datetime import date
                    if hasattr(event, 'event_date') and event.event_date:
                        days_left = (event.event_date - date.today()).days
                        days_text = str(days_left) if days_left >= 0 else f"{days_left} (prošlé)"
                        ctk.CTkLabel(self.events_frame, text=days_text).grid(
                            row=idx, column=3, padx=10, pady=2, sticky="w"
                        )
                    else:
                        ctk.CTkLabel(self.events_frame, text="N/A").grid(
                            row=idx, column=3, padx=10, pady=2, sticky="w"
                        )
                except Exception:
                    ctk.CTkLabel(self.events_frame, text="N/A").grid(
                        row=idx, column=3, padx=10, pady=2, sticky="w"
                    )

            if not upcoming:
                ctk.CTkLabel(
                    self.events_frame,
                    text="Žádné nadcházející události",
                    text_color="gray"
                ).grid(row=1, column=0, columnspan=4, pady=20)

        except Exception as e:
            ctk.CTkLabel(
                self.events_frame,
                text=f"Chyba načítání dat: {str(e)}",
                text_color="red"
            ).grid(row=1, column=0, columnspan=4, pady=20)
            # Для отладки - выведи в консоль
            import traceback
            traceback.print_exc()

    def show_all_events(self):
        print("TODO: Переход на экран всех событий")

    def add_person(self):
        print("TODO: Открыть форму добавления человека")
