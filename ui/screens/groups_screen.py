import customtkinter as ctk
from ui.screens.base_screen import BaseScreen
from ui.forms.group_form import GroupFormDialog
from repositories.group_repository import GroupRepository
from repositories.person_group_repository import PersonGroupRepository
from repositories.person_repository import PersonRepository


class GroupsScreen(BaseScreen):
    def __init__(self, parent):
        super().__init__(parent)
        self.group_repo = GroupRepository()
        self.pg_repo = PersonGroupRepository()
        self.person_repo = PersonRepository()
        self.selected_group_id = None

        # Layout: 2 колонки (список групп + детали группы)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Левая панель: Список групп
        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")
        left_frame.grid_rowconfigure(2, weight=1)

        # Заголовок
        title = ctk.CTkLabel(
            left_frame,
            text="👥 Skupiny",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, padx=0, pady=(0, 10), sticky="w")

        # Кнопки управления группами
        btn_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        btn_frame.grid(row=1, column=0, pady=10, sticky="ew")

        ctk.CTkButton(btn_frame, text="➕ Přidat", command=self.add_group, height=35, width=80).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="✏ Upravit", command=self.edit_group, height=35, width=80).pack(side="left",
                                                                                                      padx=5)
        ctk.CTkButton(btn_frame, text="🗑 Smazat", command=self.delete_group, height=35, width=80, fg_color="red").pack(
            side="left", padx=5)

        # НОВОЕ: Кнопка статистики
        ctk.CTkButton(
            btn_frame,
            text="📊 Statistiky",
            command=self.show_statistics,
            height=35,
            width=100
        ).pack(side="left", padx=5)

        # Таблица групп
        self.groups_table = ctk.CTkScrollableFrame(left_frame)
        self.groups_table.grid(row=2, column=0, pady=10, sticky="nsew")

        # Правая панель: Детали группы
        right_frame = ctk.CTkFrame(self, fg_color="transparent")
        right_frame.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")
        right_frame.grid_rowconfigure(2, weight=1)

        # Заголовок деталей
        self.detail_title = ctk.CTkLabel(
            right_frame,
            text="Vyberte skupinu",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.detail_title.grid(row=0, column=0, padx=0, pady=(0, 10), sticky="w")

        # Статистика
        self.stats_label = ctk.CTkLabel(
            right_frame,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.stats_label.grid(row=1, column=0, padx=0, pady=(0, 10), sticky="w")

        # Список людей в группе
        self.members_frame = ctk.CTkScrollableFrame(right_frame)
        self.members_frame.grid(row=2, column=0, pady=10, sticky="nsew")

        self.group_buttons = []
        self.refresh()

    def refresh(self):
        """Обновить список групп"""
        for widget in self.groups_table.winfo_children():
            widget.destroy()

        self.group_buttons = []
        self.selected_group_id = None

        # Заголовки
        headers = ["Výběr", "ID", "Název", "Počet osob"]
        for idx, header in enumerate(headers):
            label = ctk.CTkLabel(self.groups_table, text=header, font=ctk.CTkFont(weight="bold"))
            label.grid(row=0, column=idx, padx=10, pady=5, sticky="w")

        # Данные
        groups = self.group_repo.get_all_groups()
        for idx, group in enumerate(groups, start=1):
            # Подсчёт людей в группе
            members = self.pg_repo.get_persons_in_group(group.id)
            member_count = len(members)

            # Кнопка выбора
            select_btn = ctk.CTkButton(
                self.groups_table,
                text="◉",
                width=40,
                command=lambda g_id=group.id, btn_idx=idx - 1: self.select_group(g_id, btn_idx)
            )
            select_btn.grid(row=idx, column=0, padx=5, pady=2)
            self.group_buttons.append(select_btn)

            # Остальные колонки
            values = [str(group.id), group.name, str(member_count)]
            for col_idx, value in enumerate(values, start=1):
                label = ctk.CTkLabel(self.groups_table, text=value)
                label.grid(row=idx, column=col_idx, padx=10, pady=2, sticky="w")

        # Очистить детали
        self.detail_title.configure(text="Vyberte skupinu")
        self.stats_label.configure(text="")
        for widget in self.members_frame.winfo_children():
            widget.destroy()

    def select_group(self, group_id, button_index):
        """Выбрать группу и показать детали"""
        self.selected_group_id = group_id

        # Подсветка кнопки
        for idx, btn in enumerate(self.group_buttons):
            if idx == button_index:
                btn.configure(fg_color="green")
            else:
                btn.configure(fg_color=("gray75", "gray25"))

        # Обновить детали
        self.load_group_details()

    def load_group_details(self):
        """Загрузить детали группы"""
        if not self.selected_group_id:
            return

        group = self.group_repo.get_group(self.selected_group_id)
        if not group:
            return

        # Обновить заголовок
        self.detail_title.configure(text=f"👥 {group.name}")

        # Получить членов группы
        members = self.pg_repo.get_persons_in_group(self.selected_group_id)

        # Статистика
        self.stats_label.configure(text=f"Počet osob: {len(members)}")

        # Очистить список
        for widget in self.members_frame.winfo_children():
            widget.destroy()

        # Заголовок списка
        ctk.CTkLabel(
            self.members_frame,
            text="Členové skupiny:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        if not members:
            ctk.CTkLabel(
                self.members_frame,
                text="Žádní členové v této skupině",
                text_color="gray"
            ).pack(anchor="w", padx=10, pady=10)
        else:
            for person in members:
                person_frame = ctk.CTkFrame(self.members_frame)
                person_frame.pack(fill="x", padx=10, pady=2)

                birth = person.birth_date.strftime('%d.%m.%Y') if person.birth_date else 'N/A'

                ctk.CTkLabel(
                    person_frame,
                    text=f"{person.first_name} {person.last_name} ({birth})",
                    anchor="w"
                ).pack(side="left", padx=10, pady=5)

                # Кнопка удаления из группы
                ctk.CTkButton(
                    person_frame,
                    text="✗",
                    width=30,
                    fg_color="red",
                    command=lambda p_id=person.id: self.remove_person_from_group(p_id)
                ).pack(side="right", padx=5, pady=5)

        # Кнопка добавления человека в группу
        add_person_btn = ctk.CTkButton(
            self.members_frame,
            text="➕ Přidat osobu do skupiny",
            command=self.add_person_to_group_dialog
        )
        add_person_btn.pack(pady=10, padx=10, fill="x")

    def add_person_to_group_dialog(self):
        """Диалог добавления человека в группу"""
        if not self.selected_group_id:
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Přidat osobu do skupiny")
        dialog.geometry("500x400")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Vyberte osobu:",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(padx=20, pady=(20, 10))

        # Получить людей, которых ещё нет в группе
        all_persons = self.person_repo.get_all_persons()
        current_members = self.pg_repo.get_persons_in_group(self.selected_group_id)
        current_member_ids = {m.id for m in current_members}
        available_persons = [p for p in all_persons if p.id not in current_member_ids]

        if not available_persons:
            ctk.CTkLabel(
                dialog,
                text="Všechny osoby jsou již v této skupině",
                text_color="gray"
            ).pack(padx=20, pady=20)
            ctk.CTkButton(dialog, text="Zavřít", command=dialog.destroy).pack(pady=10)
            return

        # Список доступных людей
        scroll_frame = ctk.CTkScrollableFrame(dialog, height=250)
        scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        selected_person_id = [None]

        def select_person(person_id):
            selected_person_id[0] = person_id

        for person in available_persons:
            btn = ctk.CTkButton(
                scroll_frame,
                text=f"{person.first_name} {person.last_name}",
                command=lambda p_id=person.id: select_person(p_id),
                anchor="w"
            )
            btn.pack(fill="x", padx=5, pady=2)

        # Кнопка добавления
        def do_add():
            if selected_person_id[0]:
                try:
                    self.pg_repo.add_person_to_group(selected_person_id[0], self.selected_group_id)
                    dialog.destroy()
                    self.load_group_details()
                except Exception as e:
                    print(f"Chyba: {e}")

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="❌ Zrušit", command=dialog.destroy, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="➕ Přidat", command=do_add, width=100).pack(side="left", padx=5)

    def remove_person_from_group(self, person_id):
        """Удалить человека из группы"""
        if not self.selected_group_id:
            return

        try:
            self.pg_repo.remove_person_from_group(person_id, self.selected_group_id)
            self.load_group_details()
            self.refresh()  # Обновить счётчик в списке групп
        except Exception as e:
            print(f"Chyba: {e}")

    def add_group(self):
        """Добавить группу"""
        GroupFormDialog(self, on_save_callback=self.refresh)

    def edit_group(self):
        """Редактировать группу"""
        if not self.selected_group_id:
            self.show_warning("Vyberte prosím skupinu")
            return

        GroupFormDialog(self, group_id=self.selected_group_id, on_save_callback=self.refresh)

    def delete_group(self):
        """Удалить группу"""
        if not self.selected_group_id:
            self.show_warning("Vyberte prosím skupinu")
            return

        group = self.group_repo.get_group(self.selected_group_id)
        if not group:
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
            text=f"❓ Opravdu smazat skupinu?\n\n{group.name}",
            font=ctk.CTkFont(size=14),
            justify="center"
        ).pack(padx=20, pady=30)

        btn_frame = ctk.CTkFrame(confirm, fg_color="transparent")
        btn_frame.pack(pady=10)

        def do_delete():
            try:
                self.group_repo.delete_group(self.selected_group_id)
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

    def show_statistics(self):
        """Показать статистику по группам (используя VIEW)"""
        stats_window = ctk.CTkToplevel(self)
        stats_window.title("📊 Statistiky skupin")
        stats_window.geometry("1050x850")
        stats_window.resizable(False, False)
        stats_window.transient(self)
        stats_window.grab_set()

        # Заголовок
        ctk.CTkLabel(
            stats_window,
            text="📊 Statistiky skupin",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(padx=20, pady=(20, 10))

        # Описание
        ctk.CTkLabel(
            stats_window,
            text="Přehled všech skupin s počtem osob a událostí",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(padx=20, pady=(0, 10))

        # Таблица
        table_frame = ctk.CTkScrollableFrame(stats_window, height=280)
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Заголовки
        headers = ["Název skupiny", "Počet osob", "Počet událostí"]
        for idx, header in enumerate(headers):
            ctk.CTkLabel(
                table_frame,
                text=header,
                font=ctk.CTkFont(weight="bold", size=13)
            ).grid(row=0, column=idx, padx=15, pady=8, sticky="w")

        # Данные из VIEW
        try:
            stats = self.group_repo.get_group_statistics()

            if not stats:
                ctk.CTkLabel(
                    table_frame,
                    text="Žádné statistiky k zobrazení",
                    text_color="gray"
                ).grid(row=1, column=0, columnspan=3, pady=30)
            else:
                total_persons = 0
                total_events = 0

                for idx, row in enumerate(stats, start=1):
                    # Цвет строки (чередование)
                    bg_color = "gray20" if idx % 2 == 0 else "transparent"

                    values = [
                        row.group_name,
                        str(row.total_persons),
                        str(row.total_events)
                    ]

                    total_persons += row.total_persons
                    total_events += row.total_events

                    for col_idx, value in enumerate(values):
                        label = ctk.CTkLabel(
                            table_frame,
                            text=value,
                            fg_color=bg_color
                        )
                        label.grid(row=idx, column=col_idx, padx=15, pady=5, sticky="w")

                # Итоговая строка
                separator = ctk.CTkFrame(table_frame, height=2, fg_color="gray")
                separator.grid(row=len(stats) + 1, column=0, columnspan=3, sticky="ew", padx=15, pady=5)

                ctk.CTkLabel(
                    table_frame,
                    text="CELKEM:",
                    font=ctk.CTkFont(weight="bold", size=13)  # ← ИСПРАВЛЕНО
                ).grid(row=len(stats) + 2, column=0, padx=15, pady=5, sticky="w")

                ctk.CTkLabel(
                    table_frame,
                    text=str(total_persons),
                    font=ctk.CTkFont(weight="bold", size=13),
                    text_color="green"
                ).grid(row=len(stats) + 2, column=1, padx=15, pady=5, sticky="w")

                ctk.CTkLabel(
                    table_frame,
                    text=str(total_events),
                    font=ctk.CTkFont(weight="bold", size=13),
                    text_color="green"
                ).grid(row=len(stats) + 2, column=2, padx=15, pady=5, sticky="w")

        except Exception as e:
            ctk.CTkLabel(
                table_frame,
                text=f"❌ Chyba načítání statistik:\n{str(e)}",
                text_color="red"
            ).grid(row=1, column=0, columnspan=3, pady=30)
            import traceback
            traceback.print_exc()

        # Кнопка закрытия
        ctk.CTkButton(
            stats_window,
            text="Zavřít",
            command=stats_window.destroy,
            width=120,
            height=35
        ).pack(pady=(10, 20))
