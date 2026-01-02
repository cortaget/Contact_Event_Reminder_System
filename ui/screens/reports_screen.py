import customtkinter as ctk
from ui.screens.base_screen import BaseScreen
from repositories.report_repository import ReportRepository


class ReportsScreen(BaseScreen):
    def __init__(self, parent):
        super().__init__(parent)
        self.report_repo = ReportRepository()

        # Заголовок
        title = ctk.CTkLabel(
            self,
            text="📊 Reporty",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Кнопки выбора отчёта
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkButton(btn_frame, text="📅 Události (30 dní)", command=self.show_upcoming_events, height=40,
                      width=160).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="📈 Události podle skupin", command=self.show_events_by_group, height=40,
                      width=180).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🔔 Statistika upozornění", command=self.show_notifications_stats, height=40,
                      width=180).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="👥 Osoby ve skupinách", command=self.show_persons_stats, height=40,
                      width=180).pack(side="left", padx=5)

        # Область для отображения отчётов
        self.report_frame = ctk.CTkScrollableFrame(self, height=500)
        self.report_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.grid_rowconfigure(2, weight=1)

        # Показать первый отчёт по умолчанию
        self.show_upcoming_events()

    def clear_report(self):
        """Очистить область отчёта"""
        for widget in self.report_frame.winfo_children():
            widget.destroy()

    def show_upcoming_events(self):
        """Отчёт: Ближайшие события"""
        self.clear_report()

        ctk.CTkLabel(
            self.report_frame,
            text="📅 Nadcházející události (30 dní)",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 20))

        try:
            # Получить данные
            events = self.report_repo.get_upcoming_events_report(30)

            if not events:
                ctk.CTkLabel(
                    self.report_frame,
                    text="Žádné nadcházející události",
                    text_color="gray"
                ).pack(anchor="w", padx=10, pady=10)
                return

            # Таблица
            table_frame = ctk.CTkFrame(self.report_frame)
            table_frame.pack(fill="x", padx=10, pady=10)

            headers = ["Osoba", "Typ", "Datum", "Skupina"]
            for idx, header in enumerate(headers):
                label = ctk.CTkLabel(table_frame, text=header, font=ctk.CTkFont(weight="bold"))
                label.grid(row=0, column=idx, padx=10, pady=5, sticky="w")

            for idx, event in enumerate(events, start=1):
                # ИСПРАВЛЕНИЕ: безопасный доступ
                event_type = getattr(event, 'event_type', 'other')
                icon = {"birthday": "🎂", "anniversary": "💍", "other": "🎉"}.get(event_type, "🎉")

                first_name = getattr(event, 'first_name', '')
                last_name = getattr(event, 'last_name', '')
                event_date = getattr(event, 'event_date', 'N/A')
                group_name = getattr(event, 'group_name', None)

                values = [
                    f"{first_name} {last_name}",
                    f"{icon} {event_type}",
                    str(event_date),
                    group_name if group_name else "N/A"
                ]

                for col_idx, value in enumerate(values):
                    label = ctk.CTkLabel(table_frame, text=value)
                    label.grid(row=idx, column=col_idx, padx=10, pady=2, sticky="w")

            # Итоги
            ctk.CTkLabel(
                self.report_frame,
                text=f"Celkem: {len(events)} událostí",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(anchor="w", padx=10, pady=(20, 10))

        except Exception as e:
            ctk.CTkLabel(
                self.report_frame,
                text=f"Chyba načítání: {str(e)}",
                text_color="red"
            ).pack(anchor="w", padx=10, pady=10)

    def show_events_by_group(self):
        """Отчёт: События по группам"""
        self.clear_report()

        ctk.CTkLabel(
            self.report_frame,
            text="📈 Události podle skupin",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 20))

        try:
            # Получить данные
            stats = self.report_repo.get_events_statistics_by_group()

            if not stats:
                ctk.CTkLabel(
                    self.report_frame,
                    text="Žádná data",
                    text_color="gray"
                ).pack(anchor="w", padx=10, pady=10)
                return

            # Таблица
            table_frame = ctk.CTkFrame(self.report_frame)
            table_frame.pack(fill="x", padx=10, pady=10)

            headers = ["Skupina", "Počet událostí"]
            for idx, header in enumerate(headers):
                label = ctk.CTkLabel(table_frame, text=header, font=ctk.CTkFont(weight="bold"))
                label.grid(row=0, column=idx, padx=10, pady=5, sticky="w")

            total_events = 0
            for idx, row in enumerate(stats, start=1):
                group_name = getattr(row, 'group_name', None)
                event_count = getattr(row, 'event_count', 0)

                values = [group_name or "Bez skupiny", str(event_count)]
                total_events += event_count if event_count else 0

                for col_idx, value in enumerate(values):
                    label = ctk.CTkLabel(table_frame, text=value)
                    label.grid(row=idx, column=col_idx, padx=10, pady=2, sticky="w")

            # Итоги
            ctk.CTkLabel(
                self.report_frame,
                text=f"Celkem událostí: {total_events}",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(anchor="w", padx=10, pady=(20, 10))

        except Exception as e:
            ctk.CTkLabel(
                self.report_frame,
                text=f"Chyba načítání: {str(e)}",
                text_color="red"
            ).pack(anchor="w", padx=10, pady=10)

    def show_notifications_stats(self):
        """Отчёт: Статистика уведомлений"""
        self.clear_report()

        ctk.CTkLabel(
            self.report_frame,
            text="🔔 Statistika upozornění",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 20))

        try:
            # Получить данные
            stats = self.report_repo.get_notifications_statistics()

            if not stats:
                ctk.CTkLabel(
                    self.report_frame,
                    text="Žádná upozornění",
                    text_color="gray"
                ).pack(anchor="w", padx=10, pady=10)
                return

            # Таблица
            table_frame = ctk.CTkFrame(self.report_frame)
            table_frame.pack(fill="x", padx=10, pady=10)

            headers = ["Stav", "Počet"]
            for idx, header in enumerate(headers):
                label = ctk.CTkLabel(table_frame, text=header, font=ctk.CTkFont(weight="bold"))
                label.grid(row=0, column=idx, padx=10, pady=5, sticky="w")

            status_icons = {'planned': '⏳', 'sent': '✓', 'failed': '✗'}
            total_count = 0

            for idx, row in enumerate(stats, start=1):
                status = getattr(row, 'status', 'unknown')
                count = getattr(row, 'count', 0)

                icon = status_icons.get(status, '?')
                values = [f"{icon} {status}", str(count)]
                total_count += count

                for col_idx, value in enumerate(values):
                    label = ctk.CTkLabel(table_frame, text=value)
                    label.grid(row=idx, column=col_idx, padx=10, pady=2, sticky="w")

            # Итоги
            ctk.CTkLabel(
                self.report_frame,
                text=f"Celkem upozornění: {total_count}",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(anchor="w", padx=10, pady=(20, 10))

        except Exception as e:
            ctk.CTkLabel(
                self.report_frame,
                text=f"Chyba načítání: {str(e)}",
                text_color="red"
            ).pack(anchor="w", padx=10, pady=10)

    def show_persons_stats(self):
        """Отчёт: Люди в группах"""
        self.clear_report()

        ctk.CTkLabel(
            self.report_frame,
            text="👥 Osoby ve skupinách",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 20))

        try:
            # Получить данные
            stats = self.report_repo.get_persons_statistics()

            if not stats:
                ctk.CTkLabel(
                    self.report_frame,
                    text="Žádná data",
                    text_color="gray"
                ).pack(anchor="w", padx=10, pady=10)
                return

            # Таблица
            table_frame = ctk.CTkFrame(self.report_frame)
            table_frame.pack(fill="x", padx=10, pady=10)

            headers = ["Skupina", "Počet osob"]
            for idx, header in enumerate(headers):
                label = ctk.CTkLabel(table_frame, text=header, font=ctk.CTkFont(weight="bold"))
                label.grid(row=0, column=idx, padx=10, pady=5, sticky="w")

            total_persons = 0
            for idx, row in enumerate(stats, start=1):
                group_name = getattr(row, 'group_name', None)
                person_count = getattr(row, 'person_count', 0)

                values = [group_name or "Bez skupiny", str(person_count)]
                total_persons += person_count if person_count else 0

                for col_idx, value in enumerate(values):
                    label = ctk.CTkLabel(table_frame, text=value)
                    label.grid(row=idx, column=col_idx, padx=10, pady=2, sticky="w")

            # Итоги
            ctk.CTkLabel(
                self.report_frame,
                text=f"Celkem přiřazení: {total_persons}",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(anchor="w", padx=10, pady=(20, 10))

        except Exception as e:
            ctk.CTkLabel(
                self.report_frame,
                text=f"Chyba načítání: {str(e)}",
                text_color="red"
            ).pack(anchor="w", padx=10, pady=10)
