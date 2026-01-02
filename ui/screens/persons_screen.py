import customtkinter as ctk
from ui.screens.base_screen import BaseScreen
from ui.forms.person_form import PersonFormDialog
from repositories.person_repository import PersonRepository


class PersonsScreen(BaseScreen):
    def __init__(self, parent):
        super().__init__(parent)
        self.person_repo = PersonRepository()
        self.selected_person_id = None

        # Заголовок
        title = ctk.CTkLabel(
            self,
            text="🧍 Osoby",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Кнопки управления
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkButton(btn_frame, text="➕ Přidat", command=self.add_person, height=35).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="✏ Upravit", command=self.edit_person, height=35).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🗑 Smazat", command=self.delete_person, height=35, fg_color="red").pack(
            side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🔄 Obnovit", command=self.refresh, height=35).pack(side="right", padx=5)

        # Таблица
        self.table_frame = ctk.CTkScrollableFrame(self, height=500)
        self.table_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.grid_rowconfigure(2, weight=1)

        self.person_buttons = []
        self.refresh()

    def refresh(self):
        """Обновить список людей"""
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.person_buttons = []
        self.selected_person_id = None

        # Заголовки
        headers = ["Выбрать", "ID", "Jméno", "Příjmení", "Datum narození", "Pohlaví", "Aktivní"]
        for idx, header in enumerate(headers):
            label = ctk.CTkLabel(self.table_frame, text=header, font=ctk.CTkFont(weight="bold"))
            label.grid(row=0, column=idx, padx=10, pady=5, sticky="w")

        # Данные
        persons = self.person_repo.get_all_persons()
        for idx, person in enumerate(persons, start=1):
            birth = person.birth_date.strftime('%d.%m.%Y') if person.birth_date else 'N/A'
            active = "✓" if person.is_active else "✗"

            # Кнопка выбора
            select_btn = ctk.CTkButton(
                self.table_frame,
                text="◉",
                width=40,
                command=lambda p_id=person.id, btn_idx=idx - 1: self.select_person(p_id, btn_idx)
            )
            select_btn.grid(row=idx, column=0, padx=5, pady=2)
            self.person_buttons.append(select_btn)

            # Остальные колонки
            values = [
                str(person.id),
                person.first_name,
                person.last_name,
                birth,
                person.gender or 'N/A',
                active
            ]

            for col_idx, value in enumerate(values, start=1):
                label = ctk.CTkLabel(self.table_frame, text=value)
                label.grid(row=idx, column=col_idx, padx=10, pady=2, sticky="w")

    def select_person(self, person_id, button_index):
        """Выбрать человека"""
        self.selected_person_id = person_id

        # Подсветка выбранной кнопки
        for idx, btn in enumerate(self.person_buttons):
            if idx == button_index:
                btn.configure(fg_color="green")
            else:
                btn.configure(fg_color=("gray75", "gray25"))

    def add_person(self):
        """Открыть форму добавления"""
        PersonFormDialog(self, on_save_callback=self.refresh)

    def edit_person(self):
        """Редактирование"""
        if not self.selected_person_id:
            self.show_warning("Vyberte prosím osobu")
            return

        PersonFormDialog(self, person_id=self.selected_person_id, on_save_callback=self.refresh)

    def delete_person(self):
        """Удаление с подтверждением"""
        if not self.selected_person_id:
            self.show_warning("Vyberte prosím osobu")
            return

        person = self.person_repo.get_person(self.selected_person_id)
        if not person:
            return

        # Диалог подтверждения
        confirm = ctk.CTkToplevel(self)
        confirm.title("Potvrdit smazání")
        confirm.geometry("400x180")
        confirm.resizable(False, False)
        confirm.transient(self)
        confirm.grab_set()

        ctk.CTkLabel(
            confirm,
            text=f"❓ Opravdu smazat osobu?\n\n{person.first_name} {person.last_name}",
            font=ctk.CTkFont(size=14),
            justify="center"
        ).pack(padx=20, pady=30)

        btn_frame = ctk.CTkFrame(confirm, fg_color="transparent")
        btn_frame.pack(pady=10)

        def do_delete():
            try:
                self.person_repo.delete_person(self.selected_person_id)
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
