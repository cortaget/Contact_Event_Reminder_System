import customtkinter as ctk
from ui.main_window import MainWindow
from repositories.config_repository import DatabaseDeployer
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
            # Для теста: time.sleep(60)
            time.sleep(3600)

            # Проверить напоминания
            print("🔍 Проверка напоминаний...")
            reminders = notification_service.check_pending_reminders()

            if reminders:
                print(f"✅ Найдено {len(reminders)} напоминаний")
                app.after(0, lambda: show_reminders_window(app, reminders, notification_service))
            else:
                print("✅ Новых напоминаний нет")

        except Exception as e:
            print(f"❌ Ошибка фоновой проверки: {e}")


def show_reminders_window(app, reminders, notification_service):
    """Показать окно напоминаний"""
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
            app.after(2000, lambda: show_reminders_window(app, reminders, notification_service))
        else:
            print("✅ Новых напоминаний нет")

    except Exception as e:
        print(f"⚠️ Ошибка проверки напоминаний: {e}")


def check_and_deploy_database():
    """Проверить и развернуть БД если нужно"""
    deployer = DatabaseDeployer()

    print("🔍 Проверка существования базы данных...")

    if deployer.check_database_exists():
        print(f"✅ База данных найдена")
        return True

    print(f"⚠️ База данных не найдена")
    print(f"🚀 Автоматическое развёртывание базы данных...")

    success, message = deployer.deploy_database()

    if success:
        print(f"✅ {message}")
        return True
    else:
        print(f"❌ {message}")
        return False


if __name__ == "__main__":
    try:
        # Настройка внешнего вида
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        print("🚀 Запуск Event Reminder System...")

        # ===== ПРОВЕРКА И РАЗВЁРТЫВАНИЕ БД =====
        if not check_and_deploy_database():
            print("❌ Не удалось развернуть базу данных")
            print("📝 Перейдите в настройки приложения для ручной настройки")
            # Продолжаем запуск - пользователь может настроить в Settings
        # ========================================

        # Запуск основного приложения
        app = MainWindow()

        # ===== ФОНОВАЯ СИСТЕМА НАПОМИНАНИЙ =====
        app.after(1000, lambda: check_initial_reminders(app))

        reminder_thread = threading.Thread(
            target=background_reminder_checker,
            args=(app,),
            daemon=True
        )
        reminder_thread.start()
        print("✅ Фоновая система напоминаний запущена")
        # ============================================

        app.mainloop()

    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")

        # Показать ошибку в GUI
        try:
            error_window = ctk.CTk()
            error_window.title("Критическая ошибка")
            error_window.geometry("600x400")

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
            import traceback

            print("\n" + "=" * 60)
            print("ПОЛНАЯ ИНФОРМАЦИЯ ОБ ОШИБКЕ:")
            print("=" * 60)
            traceback.print_exc()
            print("=" * 60)

        sys.exit(1)
