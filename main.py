import customtkinter as ctk
from ui.main_window import MainWindow
from database_initializer import DatabaseInitializer
from ui.database_setup_window import DatabaseSetupWindow
from services.notification_service import NotificationService
from ui.reminder_notification_window import ReminderNotificationWindow
import sys
import threading
import time


def background_reminder_checker(app):
    """Фоновая проверка напоминаний каждый час"""
    notification_service = NotificationService()

    while True:
        try:
            # Подождать 1 час (3600 секунд)
            time.sleep(60)

            # Проверить напоминания
            print("🔍 Проверка напоминаний...")
            reminders = notification_service.check_pending_reminders()

            if reminders:
                print(f"✅ Найдено {len(reminders)} напоминаний")
                # Показать окно напоминаний в главном потоке
                app.after(0, lambda: show_reminders_window(app, reminders, notification_service))
            else:
                print("✅ Новых напоминаний нет")

        except Exception as e:
            print(f"❌ Ошибка фоновой проверки: {e}")


def show_reminders_window(app, reminders, notification_service):
    """Показать окно напоминаний (вызывается из главного потока)"""
    try:
        window = ReminderNotificationWindow(app, reminders, notification_service)
    except Exception as e:
        print(f"❌ Ошибка показа окна напоминаний: {e}")


def check_initial_reminders(app):
    """Проверить напоминания при запуске"""
    notification_service = NotificationService()

    try:
        print("🔍 Проверка напоминаний при запуске...")
        reminders = notification_service.check_pending_reminders()

        if reminders:
            print(f"✅ Найдено {len(reminders)} напоминаний")
            # Показать окно через 2 секунды после запуска
            app.after(2000, lambda: show_reminders_window(app, reminders, notification_service))
        else:
            print("✅ Новых напоминаний нет")

    except Exception as e:
        print(f"❌ Ошибка проверки напоминаний: {e}")


if __name__ == "__main__":
    try:
        # Настройка внешнего вида
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Проверка существования БД
        initializer = DatabaseInitializer()
        """
        if not initializer.check_database_exists():
            # База данных не найдена - показать окно инициализации
            print("⚠️ База данных не найдена. Запуск мастера настройки...")

            # Создать временное главное окно
            root = ctk.CTk()
            root.withdraw()  # Скрыть главное окно

            # Показать окно инициализации
            setup_window = DatabaseSetupWindow(parent=root)
            setup_window.run_initialization()

            # Ждать закрытия окна
            root.wait_window(setup_window)

            # Проверить успешность
            if not setup_window.success:
                print("❌ Инициализация БД не была завершена. Программа закрывается.")
                root.destroy()
                sys.exit(1)

            print("✅ База данных успешно инициализирована!")
            root.destroy()
        """
        # Запуск основного приложения
        print("🚀 Запуск основного приложения...")
        app = MainWindow()

        # ===== ФОНОВАЯ СИСТЕМА НАПОМИНАНИЙ =====

        # 1. Проверить напоминания при запуске
        app.after(1000, lambda: check_initial_reminders(app))

        # 2. Запустить фоновый поток проверки (каждый час)
        reminder_thread = threading.Thread(
            target=background_reminder_checker,
            args=(app,),
            daemon=True
        )
        reminder_thread.start()
        print("✅ Фоновая система напоминаний запущена (проверка каждый час)")

        # ============================================

        app.mainloop()

    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")

        # Показать ошибку в GUI
        try:
            error_window = ctk.CTk()
            error_window.title("Критическая ошибка")
            error_window.geometry("600x400")

            # Центрировать окно
            error_window.update_idletasks()
            x = (error_window.winfo_screenwidth() // 2) - (600 // 2)
            y = (error_window.winfo_screenheight() // 2) - (400 // 2)
            error_window.geometry(f"600x400+{x}+{y}")

            ctk.CTkLabel(
                error_window,
                text="❌ Kritická chyba",
                font=ctk.CTkFont(size=22, weight="bold"),
                text_color="red"
            ).pack(padx=20, pady=(30, 10))

            ctk.CTkLabel(
                error_window,
                text="Aplikace narazila na kritickou chybu a nemůže pokračovat.",
                font=ctk.CTkFont(size=13),
                text_color="gray"
            ).pack(padx=20, pady=(0, 20))

            error_text = ctk.CTkTextbox(error_window, height=200, width=560, font=ctk.CTkFont(size=11))
            error_text.pack(padx=20, pady=10)

            # Полная информация об ошибке
            import traceback

            full_error = f"Chyba: {str(e)}\n\n"
            full_error += "Stack trace:\n"
            full_error += traceback.format_exc()

            error_text.insert("1.0", full_error)
            error_text.configure(state="disabled")

            ctk.CTkButton(
                error_window,
                text="Zavřít",
                command=error_window.destroy,
                width=150,
                height=40,
                font=ctk.CTkFont(size=13)
            ).pack(pady=20)

            error_window.mainloop()
        except:
            # Если GUI не работает, вывести в консоль
            import traceback

            print("\n" + "=" * 60)
            print("ПОЛНАЯ ИНФОРМАЦИЯ ОБ ОШИБКЕ:")
            print("=" * 60)
            traceback.print_exc()
            print("=" * 60)

        sys.exit(1)
