import customtkinter as ctk
from models import Group
from repositories.group_repository import GroupRepository


class GroupFormDialog(ctk.CTkToplevel):
    def __init__(self, parent, group_id=None, on_save_callback=None):
        super().__init__(parent)

        self.group_repo = GroupRepository()
        self.group_id = group_id
        self.on_save_callback = on_save_callback

        self.title("Upravit skupinu" if group_id else "Přidat skupinu")
        self.geometry("500x250")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.create_widgets()

        if group_id:
            self.load_group_data()

    def create_widgets(self):
        # Заголовок
        title = ctk.CTkLabel(
            self,
            text="👥 Skupina",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(padx=20, pady=(20, 10), anchor="w")

        # Форма
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Název skupiny
        ctk.CTkLabel(form_frame, text="Název skupiny *", anchor="w").grid(
            row=0, column=0, padx=10, pady=(10, 5), sticky="w"
        )
        self.name_entry = ctk.CTkEntry(form_frame, width=400, placeholder_text="Rodina, Přátelé, Kolegové...")
        self.name_entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

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
            command=self.save_group,
            width=120
        ).pack(side="right", padx=5)

    def load_group_data(self):
        """Загрузить данные группы"""
        group = self.group_repo.get_group(self.group_id)
        if group:
            self.name_entry.insert(0, group.name)

    def save_group(self):
        """Сохранить группу"""
        name = self.name_entry.get().strip()

        if not name:
            self.show_error("Název skupiny je povinný!")
            return

        group = Group(id=self.group_id, name=name)

        try:
            if self.group_id:
                self.group_repo.update_group(group)
            else:
                self.group_repo.add_group(group)

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
