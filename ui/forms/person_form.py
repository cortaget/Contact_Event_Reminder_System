import customtkinter as ctk
from datetime import datetime
from models import Person
from repositories.person_repository import PersonRepository
from repositories.group_repository import GroupRepository
from repositories.person_group_repository import PersonGroupRepository


class PersonFormDialog(ctk.CTkToplevel):
    def __init__(self, parent, person_id=None, on_save_callback=None):
        super().__init__(parent)

        self.person_repo = PersonRepository()
        self.group_repo = GroupRepository()
        self.pg_repo = PersonGroupRepository()
        self.person_id = person_id
        self.on_save_callback = on_save_callback

        # Настройки окна
        self.title("Upravit osobu" if person_id else "Přidat osobu")
        self.geometry("600x650")
        self.resizable(False, False)

        # Центрирование окна
        self.transient(parent)
        self.grab_set()

        self.create_widgets()

        if person_id:
            self.load_person_data()

    def create_widgets(self):
        # Заголовок
        title = ctk.CTkLabel(
            self,
            text="🧍 Osobní údaje",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(padx=20, pady=(20, 10), anchor="w")

        # Форма
        form_frame = ctk.CTkScrollableFrame(self, height=450)
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Jméno
        ctk.CTkLabel(form_frame, text="Jméno *", anchor="w").grid(
            row=0, column=0, padx=10, pady=(10, 5), sticky="w"
        )
        self.first_name_entry = ctk.CTkEntry(form_frame, width=400)
        self.first_name_entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Příjmení
        ctk.CTkLabel(form_frame, text="Příjmení *", anchor="w").grid(
            row=2, column=0, padx=10, pady=(10, 5), sticky="w"
        )
        self.last_name_entry = ctk.CTkEntry(form_frame, width=400)
        self.last_name_entry.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Datum narození
        ctk.CTkLabel(form_frame, text="Datum narození (DD.MM.YYYY)", anchor="w").grid(
            row=4, column=0, padx=10, pady=(10, 5), sticky="w"
        )
        self.birth_date_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="01.01.1990")
        self.birth_date_entry.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Pohlaví
        ctk.CTkLabel(form_frame, text="Pohlaví", anchor="w").grid(
            row=6, column=0, padx=10, pady=(10, 5), sticky="w"
        )
        self.gender_var = ctk.StringVar(value="male")
        gender_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        gender_frame.grid(row=7, column=0, padx=10, pady=(0, 10), sticky="w")

        ctk.CTkRadioButton(gender_frame, text="Muž", variable=self.gender_var, value="male").pack(side="left", padx=5)
        ctk.CTkRadioButton(gender_frame, text="Žena", variable=self.gender_var, value="female").pack(side="left",
                                                                                                     padx=5)
        ctk.CTkRadioButton(gender_frame, text="Jiné", variable=self.gender_var, value="other").pack(side="left", padx=5)

        # Aktivní
        self.is_active_var = ctk.BooleanVar(value=True)
        self.is_active_checkbox = ctk.CTkCheckBox(
            form_frame,
            text="Aktivní",
            variable=self.is_active_var
        )
        self.is_active_checkbox.grid(row=8, column=0, padx=10, pady=10, sticky="w")

        # Skupiny
        ctk.CTkLabel(form_frame, text="👥 Skupiny", anchor="w", font=ctk.CTkFont(size=16, weight="bold")).grid(
            row=9, column=0, padx=10, pady=(20, 5), sticky="w"
        )

        groups_scroll = ctk.CTkScrollableFrame(form_frame, height=120)
        groups_scroll.grid(row=10, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Загрузка групп
        self.group_vars = {}
        all_groups = self.group_repo.get_all_groups()
        for group in all_groups:
            var = ctk.BooleanVar(value=False)
            checkbox = ctk.CTkCheckBox(groups_scroll, text=group.name, variable=var)
            checkbox.pack(anchor="w", padx=5, pady=2)
            self.group_vars[group.id] = var

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
            command=self.save_person,
            width=120
        ).pack(side="right", padx=5)

    def load_person_data(self):
        """Загрузить данные существующего человека"""
        person = self.person_repo.get_person(self.person_id)
        if not person:
            return

        self.first_name_entry.insert(0, person.first_name)
        self.last_name_entry.insert(0, person.last_name)

        if person.birth_date:
            self.birth_date_entry.insert(0, person.birth_date.strftime('%d.%m.%Y'))

        if person.gender:
            self.gender_var.set(person.gender)

        self.is_active_var.set(person.is_active)

        # Загрузить группы человека
        person_groups = self.pg_repo.get_groups_for_person(self.person_id)
        for group in person_groups:
            if group.id in self.group_vars:
                self.group_vars[group.id].set(True)

    def save_person(self):
        """Сохранить человека"""
        # Валидация
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()

        if not first_name or not last_name:
            self.show_error("Jméno a příjmení jsou povinné!")
            return

        # Парсинг даты
        birth_date = None
        birth_date_str = self.birth_date_entry.get().strip()
        if birth_date_str:
            try:
                birth_date = datetime.strptime(birth_date_str, '%d.%m.%Y').date()
            except ValueError:
                self.show_error("Neplatný formát data! Použijte DD.MM.YYYY")
                return

        # Создание/обновление Person
        person = Person(
            id=self.person_id,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            gender=self.gender_var.get(),
            is_active=self.is_active_var.get()
        )

        try:
            if self.person_id:
                self.person_repo.update_person(person)
                person_id = self.person_id
            else:
                person_id = self.person_repo.add_person(person)

            # Обновление групп
            # Удаляем старые связи
            if self.person_id:
                current_groups = self.pg_repo.get_groups_for_person(self.person_id)
                for group in current_groups:
                    self.pg_repo.remove_person_from_group(self.person_id, group.id)

            # Добавляем новые
            for group_id, var in self.group_vars.items():
                if var.get():
                    self.pg_repo.add_person_to_group(person_id, group_id)

            # Callback
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
