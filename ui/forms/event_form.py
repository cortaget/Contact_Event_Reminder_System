import customtkinter as ctk
from datetime import datetime
from models import Event
from repositories.event_repository import EventRepository
from repositories.person_repository import PersonRepository


class EventFormDialog(ctk.CTkToplevel):
    def __init__(self, parent, event_id=None, on_save_callback=None):
        super().__init__(parent)

        self.event_repo = EventRepository()
        self.person_repo = PersonRepository()
        self.event_id = event_id
        self.on_save_callback = on_save_callback

        self.title("Upravit událost" if event_id else "Přidat událost")
        self.geometry("550x550")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.create_widgets()

        if event_id:
            self.load_event_data()

    def create_widgets(self):
        # Заголовок
        title = ctk.CTkLabel(
            self,
            text="🎉 Událost",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(padx=20, pady=(20, 10), anchor="w")

        # Форма
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Osoba (выбор из списка)
        ctk.CTkLabel(form_frame, text="Osoba *", anchor="w").grid(
            row=0, column=0, padx=10, pady=(10, 5), sticky="w"
        )

        persons = self.person_repo.get_all_persons()
        self.person_dict = {f"{p.first_name} {p.last_name} (ID: {p.id})": p.id for p in persons}
        person_names = list(self.person_dict.keys())

        self.person_combo = ctk.CTkComboBox(
            form_frame,
            values=person_names if person_names else ["Žádné osoby"],
            width=400,
            state="readonly"
        )
        self.person_combo.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        if person_names:
            self.person_combo.set(person_names[0])

        # Typ události
        ctk.CTkLabel(form_frame, text="Typ události *", anchor="w").grid(
            row=2, column=0, padx=10, pady=(10, 5), sticky="w"
        )

        self.event_type_var = ctk.StringVar(value="birthday")
        type_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        type_frame.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="w")

        ctk.CTkRadioButton(type_frame, text="🎂 Narozeniny", variable=self.event_type_var, value="birthday").pack(
            side="left", padx=5)
        ctk.CTkRadioButton(type_frame, text="💍 Výročí", variable=self.event_type_var, value="anniversary").pack(
            side="left", padx=5)
        ctk.CTkRadioButton(type_frame, text="🎉 Jiné", variable=self.event_type_var, value="other").pack(side="left",
                                                                                                        padx=5)

        # Datum události
        ctk.CTkLabel(form_frame, text="Datum události (DD.MM.YYYY) *", anchor="w").grid(
            row=4, column=0, padx=10, pady=(10, 5), sticky="w"
        )
        self.event_date_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="15.05.2026")
        self.event_date_entry.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Připomenutí (дней до события)
        ctk.CTkLabel(form_frame, text="Připomenout za (dní) *", anchor="w").grid(
            row=6, column=0, padx=10, pady=(10, 5), sticky="w"
        )
        self.reminder_days_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="7")
        self.reminder_days_entry.insert(0, "7")
        self.reminder_days_entry.grid(row=7, column=0, padx=10, pady=(0, 10), sticky="ew")

        form_frame.grid_columnconfigure(0, weight=1)

        # Кнопки
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(padx=20, pady=20, fill="x")

        ctk.CTkButton(
            btn_frame,
            text="❌ Zrušit",
            command=self.destroy,
            fg_color="gray",
            width=120
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="💾 Uložit",
            command=self.save_event,
            width=120
        ).pack(side="right", padx=5)

    def load_event_data(self):
        """Загрузить данные существующего события"""
        event = self.event_repo.get_event(self.event_id)
        if not event:
            return

        # Найти и установить Person
        person = self.person_repo.get_person(event.person_id)
        if person:
            person_str = f"{person.first_name} {person.last_name} (ID: {person.id})"
            if person_str in self.person_dict:
                self.person_combo.set(person_str)

        # Тип события
        self.event_type_var.set(event.event_type)

        # Дата
        if event.event_date:
            self.event_date_entry.delete(0, 'end')
            self.event_date_entry.insert(0, event.event_date.strftime('%d.%m.%Y'))

        # Дни напоминания
        self.reminder_days_entry.delete(0, 'end')
        self.reminder_days_entry.insert(0, str(event.reminder_days_before))

    def save_event(self):
        """Сохранить событие"""
        # Валидация
        selected_person_str = self.person_combo.get()
        if selected_person_str not in self.person_dict:
            self.show_error("Vyberte prosím osobu!")
            return

        person_id = self.person_dict[selected_person_str]

        # Парсинг даты
        event_date_str = self.event_date_entry.get().strip()
        if not event_date_str:
            self.show_error("Datum události je povinné!")
            return

        try:
            event_date = datetime.strptime(event_date_str, '%d.%m.%Y').date()
        except ValueError:
            self.show_error("Neplatný formát data! Použijte DD.MM.YYYY")
            return

        # Дни напоминания
        try:
            reminder_days = int(self.reminder_days_entry.get().strip())
            if reminder_days < 0:
                raise ValueError
        except ValueError:
            self.show_error("Počet dní musí být kladné číslo!")
            return

        # Создание/обновление Event
        event = Event(
            id=self.event_id,
            person_id=person_id,
            event_type=self.event_type_var.get(),
            event_date=event_date,
            reminder_days_before=reminder_days
        )

        try:
            if self.event_id:
                self.event_repo.update_event(event)
            else:
                self.event_repo.add_event(event)

            if self.on_save_callback:
                self.on_save_callback()

            self.destroy()

        except Exception as e:
            self.show_error(f"Chyba při ukládání: {str(e)}")

    def show_error(self, message):
        """Показать ошибку"""
        error_window = ctk.CTkToplevel(self)
        error_window.title("Chyba")
        error_window.geometry("400x150")
        error_window.resizable(False, False)
        error_window.transient(self)
        error_window.grab_set()

        ctk.CTkLabel(
            error_window,
            text="❌ " + message,
            font=ctk.CTkFont(size=14),
            wraplength=350
        ).pack(padx=20, pady=30)

        ctk.CTkButton(
            error_window,
            text="OK",
            command=error_window.destroy,
            width=100
        ).pack(pady=10)
