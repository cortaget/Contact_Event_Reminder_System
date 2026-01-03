import customtkinter as ctk
from datetime import datetime
from models import Event
from repositories.event_repository import EventRepository
from repositories.person_repository import PersonRepository
from repositories.event_type_repository import EventTypeRepository


class EventFormDialog(ctk.CTkToplevel):
    def __init__(self, parent, event_id=None, on_save_callback=None):
        super().__init__(parent)

        self.event_repo = EventRepository()
        self.person_repo = PersonRepository()
        self.event_type_repo = EventTypeRepository()
        self.event_id = event_id
        self.on_save_callback = on_save_callback

        self.title("Upravit událost" if event_id else "Přidat událost")
        self.geometry("550x600")
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
        form_frame = ctk.CTkScrollableFrame(self, height=400)
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Osoba
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
        # Typ události
        ctk.CTkLabel(form_frame, text="Typ události *", anchor="w").grid(
            row=2, column=0, padx=10, pady=(10, 5), sticky="w"
        )

        # Создаём контейнер для ComboBox + кнопка
        type_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        type_frame.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew")

        # ComboBox с типами
        event_types = self.event_type_repo.get_all()
        self.event_type_map = {et.name: et.id for et in event_types}
        type_names = list(self.event_type_map.keys())

        self.event_type_combo = ctk.CTkComboBox(
            type_frame,
            values=type_names if type_names else ["birthday"],
            width=300,
            state="readonly"
        )
        self.event_type_combo.pack(side="left", padx=(0, 5))
        if type_names:
            self.event_type_combo.set(type_names[0])

        # Кнопка добавления нового типа
        ctk.CTkButton(
            type_frame,
            text="+ Nový typ",
            command=self.add_new_event_type,
            width=90,
            fg_color="green"
        ).pack(side="left")

        # Datum události
        ctk.CTkLabel(form_frame, text="Datum události (DD.MM.YYYY) *", anchor="w").grid(
            row=4, column=0, padx=10, pady=(10, 5), sticky="w"
        )
        self.event_date_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="15.05.2026")
        self.event_date_entry.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Připomenout za (dní)
        ctk.CTkLabel(form_frame, text="Připomenout za (dní) *", anchor="w").grid(
            row=6, column=0, padx=10, pady=(10, 5), sticky="w"
        )
        self.reminder_days_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="7")
        self.reminder_days_entry.insert(0, "7")
        self.reminder_days_entry.grid(row=7, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Čas upozornění
        ctk.CTkLabel(form_frame, text="Čas upozornění (HH:MM)", anchor="w").grid(
            row=8, column=0, padx=10, pady=(10, 5), sticky="w"
        )
        self.reminder_time_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="09:00")
        self.reminder_time_entry.insert(0, "09:00")
        self.reminder_time_entry.grid(row=9, column=0, padx=10, pady=(0, 10), sticky="ew")

        form_frame.grid_columnconfigure(0, weight=1)

        # Кнопки
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(padx=20, pady=(5, 10), fill="x")

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

        # Person
        person = self.person_repo.get_person(event.person_id)
        if person:
            person_str = f"{person.first_name} {person.last_name} (ID: {person.id})"
            if person_str in self.person_dict:
                self.person_combo.set(person_str)

        # Тип события
        if event.event_type_id:
            event_type = self.event_type_repo.get_by_id(event.event_type_id)
            if event_type and event_type.name in self.event_type_map:
                self.event_type_combo.set(event_type.name)

        # Дата
        if event.event_date:
            self.event_date_entry.delete(0, 'end')
            self.event_date_entry.insert(0, event.event_date.strftime('%d.%m.%Y'))

        # Дни напоминания
        self.reminder_days_entry.delete(0, 'end')
        self.reminder_days_entry.insert(0, str(event.reminder_days_before))

        # Время напоминания
        if event.reminder_time:
            self.reminder_time_entry.delete(0, 'end')
            self.reminder_time_entry.insert(0, event.reminder_time.strftime('%H:%M'))

    def save_event(self):
        """Сохранить событие"""
        # Person
        selected_person_str = self.person_combo.get()
        if selected_person_str not in self.person_dict:
            self.show_error("Vyberte prosím osobu!")
            return

        person_id = self.person_dict[selected_person_str]

        # Тип события
        event_type_name = self.event_type_combo.get()
        event_type_id = self.event_type_map.get(event_type_name)
        if not event_type_id:
            self.show_error("Vyberte typ události!")
            return

        # Дата
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

        # Время напоминания
        reminder_time = None
        time_str = self.reminder_time_entry.get().strip()
        if time_str:
            try:
                reminder_time = datetime.strptime(time_str, '%H:%M').time()
            except ValueError:
                self.show_error("Neplatný čas! Použijte formát HH:MM (např. 17:45)")
                return

        # Создание события
        event = Event(
            id=self.event_id,
            person_id=person_id,
            event_type_id=event_type_id,
            event_date=event_date,
            reminder_days_before=reminder_days,
            reminder_time=reminder_time
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

    def add_new_event_type(self):
        """Добавить новый тип события"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Přidat typ události")
        dialog.geometry("400x220")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="🎉 Nový typ události",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(padx=20, pady=(20, 10))

        ctk.CTkLabel(
            dialog,
            text="Název typu:",
            anchor="w"
        ).pack(padx=20, pady=(10, 5), anchor="w")

        name_entry = ctk.CTkEntry(dialog, width=360, placeholder_text="Např: wedding, graduation, meeting...")
        name_entry.pack(padx=20, pady=(0, 10))

        # Информация
        ctk.CTkLabel(
            dialog,
            text="💡 Tip: Použijte anglické názvy (birthday, wedding...)",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(padx=20, pady=(0, 10))

        def save_type():
            name = name_entry.get().strip().lower()
            if not name:
                error = ctk.CTkLabel(dialog, text="❌ Název je povinný!", text_color="red")
                error.pack(padx=20, pady=5)
                return

            try:
                # Добавляем в БД
                new_id = self.event_type_repo.add(name)

                # Обновляем ComboBox
                self.event_type_map[name] = new_id
                type_names = list(self.event_type_map.keys())
                self.event_type_combo.configure(values=type_names)
                self.event_type_combo.set(name)  # Выбираем новый тип

                dialog.destroy()

                # Показать успех
                success_dialog = ctk.CTkToplevel(self)
                success_dialog.title("Úspěch")
                success_dialog.geometry("300x120")
                success_dialog.resizable(False, False)
                success_dialog.transient(self)
                success_dialog.grab_set()

                ctk.CTkLabel(
                    success_dialog,
                    text=f"✅ Typ '{name}' byl přidán!",
                    font=ctk.CTkFont(size=14)
                ).pack(padx=20, pady=20)

                ctk.CTkButton(
                    success_dialog,
                    text="OK",
                    command=success_dialog.destroy,
                    width=100
                ).pack(pady=10)

            except Exception as e:
                error = ctk.CTkLabel(dialog, text=f"❌ Chyba: {str(e)}", text_color="red")
                error.pack(padx=20, pady=5)

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(padx=20, pady=10)

        ctk.CTkButton(btn_frame, text="❌ Zrušit", command=dialog.destroy, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="💾 Uložit", command=save_type, width=100, fg_color="green").pack(side="left",
                                                                                                       padx=5)

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
