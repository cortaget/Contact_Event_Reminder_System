import customtkinter as ctk
from ui.screens.base_screen import BaseScreen
from ui.forms.event_form import EventFormDialog
from repositories.event_repository import EventRepository
from repositories.person_repository import PersonRepository


class EventsScreen(BaseScreen):
    def __init__(self, parent):
        super().__init__(parent)
        self.event_repo = EventRepository()
        self.person_repo = PersonRepository()
        self.selected_event_id = None

        # Заголовок
        title = ctk.CTkLabel(
            self,
            text="🎉 Události",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Кнопки управления
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkButton(btn_frame, text="➕ Přidat", command=self.add_event, height=35).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="✏ Upravit", command=self.edit_event, height=35).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🗑 Smazat", command=self.delete_event, height=35, fg_color="red").pack(
            side="left", padx=5)

        # Фильтр
        ctk.CTkLabel(btn_frame, text="Filtr:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(30, 5))

        self.filter_var = ctk.StringVar(value="all")
        ctk.CTkRadioButton(btn_frame, text="Všechny", variable=self.filter_var, value="all", command=self.refresh).pack(
            side="left", padx=2)
        ctk.CTkRadioButton(btn_frame, text="30 dní", variable=self.filter_var, value="30", command=self.refresh).pack(
            side="left", padx=2)
        ctk.CTkRadioButton(btn_frame, text="90 dní", variable=self.filter_var, value="90", command=self.refresh).pack(
            side="left", padx=2)

        ctk.CTkButton(btn_frame, text="🔄 Obnovit", command=self.refresh, height=35).pack(side="right", padx=5)

        # Таблица
        self.table_frame = ctk.CTkScrollableFrame(self, height=500)
        self.table_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.grid_rowconfigure(2, weight=1)

        self.event_buttons = []
        self.refresh()

    def refresh(self):
        """Обновить список событий"""
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.event_buttons = []
        self.selected_event_id = None

        # Заголовки
        headers = ["Výběr", "ID", "Osoba", "Typ", "Datum", "Připomenutí (dní)"]
        for idx, header in enumerate(headers):
            label = ctk.CTkLabel(self.table_frame, text=header, font=ctk.CTkFont(weight="bold"))
            label.grid(row=0, column=idx, padx=10, pady=5, sticky="w")

        # Данные
        filter_type = self.filter_var.get()
        if filter_type == "all":
            events = self.event_repo.get_all_events()
        else:
            days = int(filter_type)
            events = self.event_repo.get_upcoming_events(days)

        # Словарь людей для быстрого доступа
        persons_dict = {p.id: p for p in self.person_repo.get_all_persons()}

        for idx, event in enumerate(events, start=1):
            person = persons_dict.get(event.person_id)
            person_name = f"{person.first_name} {person.last_name}" if person else f"ID: {event.person_id}"

            event_date_str = event.event_date.strftime('%d.%m.%Y') if event.event_date else 'N/A'

            # Иконка типа
            icon = {"birthday": "🎂", "anniversary": "💍", "other": "🎉"}.get(event.event_type, "🎉")

            # Кнопка выбора
            select_btn = ctk.CTkButton(
                self.table_frame,
                text="◉",
                width=40,
                command=lambda e_id=event.id, btn_idx=idx - 1: self.select_event(e_id, btn_idx)
            )
            select_btn.grid(row=idx, column=0, padx=5, pady=2)
            self.event_buttons.append(select_btn)

            # Остальные колонки
            values = [
                str(event.id),
                person_name,
                f"{icon} {event.event_type}",
                event_date_str,
                str(event.reminder_days_before)
            ]

            for col_idx, value in enumerate(values, start=1):
                label = ctk.CTkLabel(self.table_frame, text=value)
                label.grid(row=idx, column=col_idx, padx=10, pady=2, sticky="w")

    def select_event(self, event_id, button_index):
        """Выбрать событие"""
        self.selected_event_id = event_id

        for idx, btn in enumerate(self.event_buttons):
            if idx == button_index:
                btn.configure(fg_color="green")
            else:
                btn.configure(fg_color=("gray75", "gray25"))

    def add_event(self):
        """Добавить событие"""
        EventFormDialog(self, on_save_callback=self.refresh)

    def edit_event(self):
        """Редактировать событие"""
        if not self.selected_event_id:
            self.show_warning("Vyberte prosím událost")
            return

        EventFormDialog(self, event_id=self.selected_event_id, on_save_callback=self.refresh)

    def delete_event(self):
        """Удалить событие"""
        if not self.selected_event_id:
            self.show_warning("Vyberte prosím událost")
            return

        event = self.event_repo.get_event(self.selected_event_id)
        if not event:
            return

        # Диалог подтверждения
        confirm = ctk.CTkToplevel(self)
        confirm.title("Potvrdit smazání")
        confirm.geometry("400x180")
        confirm.resizable(False, False)
        confirm.transient(self)
        confirm.grab_set()

        person = self.person_repo.get_person(event.person_id)
        person_name = f"{person.first_name} {person.last_name}" if person else f"ID: {event.person_id}"

        ctk.CTkLabel(
            confirm,
            text=f"❓ Opravdu smazat událost?\n\n{event.event_type} - {person_name}\n{event.event_date}",
            font=ctk.CTkFont(size=14),
            justify="center"
        ).pack(padx=20, pady=30)

        btn_frame = ctk.CTkFrame(confirm, fg_color="transparent")
        btn_frame.pack(pady=10)

        def do_delete():
            try:
                self.event_repo.delete_event(self.selected_event_id)
                confirm.destroy()
                self.refresh()
            except Exception as e:
                self.show_warning(f"Chyba: {str(e)}")

        ctk.CTkButton(btn_frame, text="❌ Zrušit", command=confirm.destroy, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🗑 Smazat", command=do_delete, fg_color="red", width=100).pack(side="left",
                                                                                                     padx=5)

    def show_warning(self, message):
        """Показать предупреждение"""
        warning = ctk.CTkToplevel(self)
        warning.title("Varování")
        warning.geometry("400x150")
        warning.resizable(False, False)
        warning.transient(self)
        warning.grab_set()

        ctk.CTkLabel(
            warning,
            text="⚠️ " + message,
            font=ctk.CTkFont(size=14)
        ).pack(padx=20, pady=30)

        ctk.CTkButton(warning, text="OK", command=warning.destroy, width=100).pack(pady=10)
