import customtkinter as ctk
from ui.main_window import MainWindow
from ui.database_setup_window import show_database_setup
from database_initializer import DatabaseInitializer
import sys

if __name__ == "__main__":
    try:
        # Проверка существования БД
        initializer = DatabaseInitializer()

        if not initializer.check_database_exists():
            # Показать GUI окно инициализации
            success = show_database_setup()

            if not success:
                # Если не удалось создать БД - выйти
                sys.exit(1)

        # Настройка внешнего вида
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Запуск основного приложения
        app = MainWindow()
        app.mainloop()

    except Exception as e:
        # Показать ошибку в GUI
        error_window = ctk.CTk()
        error_window.title("Критическая ошибка")
        error_window.geometry("500x300")

        ctk.CTkLabel(
            error_window,
            text="❌ Критическая ошибка",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="red"
        ).pack(padx=20, pady=(20, 10))

        error_text = ctk.CTkTextbox(error_window, height=150, width=460)
        error_text.pack(padx=20, pady=10)
        error_text.insert("1.0", str(e))
        error_text.configure(state="disabled")

        ctk.CTkButton(
            error_window,
            text="Закрыть",
            command=error_window.destroy,
            width=100
        ).pack(pady=10)

        error_window.mainloop()
        sys.exit(1)
