import customtkinter as ctk
from ui.screens.base_screen import BaseScreen
from tkinter import filedialog
from services.import_service import ImportService
import json
import csv


class ImportScreen(BaseScreen):
    def __init__(self, parent):
        super().__init__(parent)
        self.import_service = ImportService()

        # Заголовок
        title = ctk.CTkLabel(
            self,
            text="📥 Import dat",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Главный контейнер
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # === БЛОК 1: Import osob (CSV) ===
        persons_frame = ctk.CTkFrame(main_frame)
        persons_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        ctk.CTkLabel(
            persons_frame,
            text="🧍 Import osob z CSV",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))

        ctk.CTkLabel(
            persons_frame,
            text="Formát: first_name,last_name,birth_date,gender,is_active",
            text_color="gray",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=15, pady=(0, 5))

        ctk.CTkLabel(
            persons_frame,
            text="Příklad: Jan,Novák,1990-05-15,male,1",
            text_color="gray",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=15, pady=(0, 10))

        self.persons_file_label = ctk.CTkLabel(
            persons_frame,
            text="Žádný soubor vybrán",
            text_color="gray"
        )
        self.persons_file_label.pack(anchor="w", padx=15, pady=5)

        btn_frame1 = ctk.CTkFrame(persons_frame, fg_color="transparent")
        btn_frame1.pack(anchor="w", padx=15, pady=(5, 15))

        ctk.CTkButton(
            btn_frame1,
            text="📂 Vybrat CSV soubor",
            command=self.select_persons_file,
            width=150
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame1,
            text="▶ Importovat",
            command=self.import_persons,
            width=120,
            fg_color="green"
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame1,
            text="📄 Vytvořit vzor",
            command=self.create_persons_template,
            width=130
        ).pack(side="left", padx=5)

        # === БЛОК 2: Import událostí (JSON) ===
        events_frame = ctk.CTkFrame(main_frame)
        events_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        ctk.CTkLabel(
            events_frame,
            text="🎉 Import událostí z JSON",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))

        ctk.CTkLabel(
            events_frame,
            text='Formát: [{"person_id": 1, "event_type": "birthday", "event_date": "2026-05-15", "reminder_days_before": 7}]',
            text_color="gray",
            font=ctk.CTkFont(size=12),
            wraplength=700
        ).pack(anchor="w", padx=15, pady=(0, 10))

        self.events_file_label = ctk.CTkLabel(
            events_frame,
            text="Žádný soubor vybrán",
            text_color="gray"
        )
        self.events_file_label.pack(anchor="w", padx=15, pady=5)

        btn_frame2 = ctk.CTkFrame(events_frame, fg_color="transparent")
        btn_frame2.pack(anchor="w", padx=15, pady=(5, 15))

        ctk.CTkButton(
            btn_frame2,
            text="📂 Vybrat JSON soubor",
            command=self.select_events_file,
            width=150
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame2,
            text="▶ Importovat",
            command=self.import_events,
            width=120,
            fg_color="green"
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame2,
            text="📄 Vytvořit vzor",
            command=self.create_events_template,
            width=130
        ).pack(side="left", padx=5)

        # === БЛОК 3: Import skupin (JSON) ===
        groups_frame = ctk.CTkFrame(main_frame)
        groups_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        ctk.CTkLabel(
            groups_frame,
            text="👥 Import skupin z JSON",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))

        ctk.CTkLabel(
            groups_frame,
            text='Formát: {"groups": [{"name": "Rodina"}, {"name": "Přátelé"}]}',
            text_color="gray",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=15, pady=(0, 10))

        self.groups_file_label = ctk.CTkLabel(
            groups_frame,
            text="Žádný soubor vybrán",
            text_color="gray"
        )
        self.groups_file_label.pack(anchor="w", padx=15, pady=5)

        btn_frame3 = ctk.CTkFrame(groups_frame, fg_color="transparent")
        btn_frame3.pack(anchor="w", padx=15, pady=(5, 15))

        ctk.CTkButton(
            btn_frame3,
            text="📂 Vybrat JSON soubor",
            command=self.select_groups_file,
            width=150
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame3,
            text="▶ Importovat",
            command=self.import_groups,
            width=120,
            fg_color="green"
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame3,
            text="📄 Vytvořit vzor",
            command=self.create_groups_template,
            width=130
        ).pack(side="left", padx=5)

        # Переменные для хранения путей к файлам
        self.persons_file_path = None
        self.events_file_path = None
        self.groups_file_path = None

    def select_persons_file(self):
        """Выбрать CSV файл с людьми"""
        file_path = filedialog.askopenfilename(
            title="Vyberte CSV soubor",
            filetypes=[("CSV soubory", "*.csv"), ("Všechny soubory", "*.*")]
        )
        if file_path:
            self.persons_file_path = file_path
            self.persons_file_label.configure(text=f"Vybrán: {file_path.split('/')[-1]}")

    def select_events_file(self):
        """Выбрать JSON файл с событиями"""
        file_path = filedialog.askopenfilename(
            title="Vyberte JSON soubor",
            filetypes=[("JSON soubory", "*.json"), ("Všechny soubory", "*.*")]
        )
        if file_path:
            self.events_file_path = file_path
            self.events_file_label.configure(text=f"Vybrán: {file_path.split('/')[-1]}")

    def select_groups_file(self):
        """Выбрать JSON файл с группами"""
        file_path = filedialog.askopenfilename(
            title="Vyberte JSON soubor",
            filetypes=[("JSON soubory", "*.json"), ("Všechny soubory", "*.*")]
        )
        if file_path:
            self.groups_file_path = file_path
            self.groups_file_label.configure(text=f"Vybrán: {file_path.split('/')[-1]}")

    def import_persons(self):
        """Импорт людей из CSV"""
        if not self.persons_file_path:
            self.show_message("Chyba", "Nejprve vyberte CSV soubor!")
            return

        try:
            result = self.import_service.import_persons_from_csv(self.persons_file_path)
            if result:
                self.show_message("Úspěch", "Osoby byly úspěšně importovány!", success=True)
            else:
                self.show_message("Chyba", "Import selhal!")
        except Exception as e:
            self.show_message("Chyba", f"Chyba při importu:\n{str(e)}")

    def import_events(self):
        """Импорт событий из JSON"""
        if not self.events_file_path:
            self.show_message("Chyba", "Nejprve vyberte JSON soubor!")
            return

        try:
            result = self.import_service.import_events_from_json(self.events_file_path)
            if result:
                self.show_message("Úspěch", "Události byly úspěšně importovány!", success=True)
            else:
                self.show_message("Chyba", "Import selhal!")
        except Exception as e:
            self.show_message("Chyba", f"Chyba při importu:\n{str(e)}")

    def import_groups(self):
        """Импорт групп из JSON"""
        if not self.groups_file_path:
            self.show_message("Chyba", "Nejprve vyberte JSON soubor!")
            return

        try:
            result = self.import_service.import_groups_from_json(self.groups_file_path)
            if result:
                self.show_message("Úspěch", "Skupiny byly úspěšně importovány!", success=True)
            else:
                self.show_message("Chyba", "Import selhal!")
        except Exception as e:
            self.show_message("Chyba", f"Chyba při importu:\n{str(e)}")

    def create_persons_template(self):
        """Создать шаблон CSV для людей"""
        file_path = filedialog.asksaveasfilename(
            title="Uložit vzorový CSV soubor",
            defaultextension=".csv",
            filetypes=[("CSV soubory", "*.csv")]
        )
        if file_path:
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['first_name', 'last_name', 'birth_date', 'gender', 'is_active'])
                writer.writerow(['Jan', 'Novák', '1990-05-15', 'male', '1'])
                writer.writerow(['Marie', 'Nováková', '1992-08-20', 'female', '1'])

            self.show_message("Úspěch", f"Vzor byl vytvořen:\n{file_path}", success=True)

    def create_events_template(self):
        """Создать шаблон JSON для событий"""
        file_path = filedialog.asksaveasfilename(
            title="Uložit vzorový JSON soubor",
            defaultextension=".json",
            filetypes=[("JSON soubory", "*.json")]
        )
        if file_path:
            template = [
                {
                    "person_id": 1,
                    "event_type": "birthday",
                    "event_date": "2026-05-15",
                    "reminder_days_before": 7
                },
                {
                    "person_id": 2,
                    "event_type": "anniversary",
                    "event_date": "2026-06-20",
                    "reminder_days_before": 14
                }
            ]
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=4, ensure_ascii=False)

            self.show_message("Úspěch", f"Vzor byl vytvořen:\n{file_path}", success=True)

    def create_groups_template(self):
        """Создать шаблон JSON для групп"""
        file_path = filedialog.asksaveasfilename(
            title="Uložit vzorový JSON soubor",
            defaultextension=".json",
            filetypes=[("JSON soubory", "*.json")]
        )
        if file_path:
            template = {
                "groups": [
                    {"name": "Rodina"},
                    {"name": "Přátelé"},
                    {"name": "Kolegové"}
                ]
            }
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=4, ensure_ascii=False)

            self.show_message("Úspěch", f"Vzor byl vytvořen:\n{file_path}", success=True)

    def show_message(self, title, message, success=False):
        """Показать сообщение"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("500x200")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        icon = "✅" if success else "❌"

        ctk.CTkLabel(
            dialog,
            text=f"{icon} {message}",
            font=ctk.CTkFont(size=14),
            wraplength=450
        ).pack(padx=20, pady=30)

        ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy,
            width=100
        ).pack(pady=10)
