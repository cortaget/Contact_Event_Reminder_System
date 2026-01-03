import customtkinter as ctk
from ui.screens.base_screen import BaseScreen
from repositories.notification_repository import NotificationRepository
from repositories.event_repository import EventRepository
from repositories.person_repository import PersonRepository
from models import Notification
from datetime import datetime


class NotificationsScreen(BaseScreen):
    def __init__(self, parent):
        super().__init__(parent)
        self.notification_repo = NotificationRepository()
        self.event_repo = EventRepository()
        self.person_repo = PersonRepository()
        self.selected_notification_id = None

        # Заголовок
        title = ctk.CTkLabel(
            self,
            text="🔔 Upozornění",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Кнопки управления
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkButton(btn_frame, text="➕ Vytvořit testovací", command=self.create_test_notification, height=35).pack(
            side="left", padx=5)
        ctk.CTkButton(btn_frame, text="🔄 Znovu odeslat", command=self.resend_notification, height=35).pack(side="left",
                                                                                                           padx=5)
        ctk.CTkButton(btn_frame, text="🗑 Smazat", command=self.delete_notification, height=35, fg_color="red").pack(
            side="left", padx=5)

        # Фильтр по статусу
        ctk.CTkLabel(btn_frame, text="Filtr:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(30, 5))

        self.filter_var = ctk.StringVar(value="all")
        ctk.CTkRadioButton(btn_frame, text="Všechny", variable=self.filter_var, value="all", command=self.refresh).pack(
            side="left", padx=2)
        ctk.CTkRadioButton(btn_frame, text="⏳ Plánované", variable=self.filter_var, value="planned",
                           command=self.refresh).pack(side="left", padx=2)
        ctk.CTkRadioButton(btn_frame, text="✓ Odesláno", variable=self.filter_var, value="sent",
                           command=self.refresh).pack(side="left", padx=2)
        ctk.CTkRadioButton(btn_frame, text="✗ Chyba", variable=self.filter_var, value="failed",
                           command=self.refresh).pack(side="left", padx=2)

        ctk.CTkButton(btn_frame, text="🔄 Obnovit", command=self.refresh, height=35).pack(side="right", padx=5)

        # Таблица
        self.table_frame = ctk.CTkScrollableFrame(self, height=500)
        self.table_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.grid_rowconfigure(2, weight=1)

        self.notification_buttons = []
        self.refresh()

    def refresh(self):
        """Обновить список уведомлений"""
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.notification_buttons = []
        self.selected_notification_id = None

        # Заголовки
        headers = ["Výběr", "ID", "Událost", "Osoba", "Datum odeslání", "Stav"]
        for idx, header in enumerate(headers):
            label = ctk.CTkLabel(self.table_frame, text=header, font=ctk.CTkFont(weight="bold"))
            label.grid(row=0, column=idx, padx=10, pady=5, sticky="w")

        try:
            # Получить уведомления с фильтрацией
            filter_type = self.filter_var.get()
            if filter_type == "all":
                notifications = self.notification_repo.get_all_notifications()
            elif filter_type == "planned":
                notifications = self.notification_repo.get_pending_notifications()
            else:
                all_notifications = self.notification_repo.get_all_notifications()
                notifications = [n for n in all_notifications if n.status == filter_type]

            # Кэш событий и людей
            events_cache = {}
            persons_cache = {}

            # Импорт для работы с типами событий
            from repositories.event_type_repository import EventTypeRepository
            event_type_repo = EventTypeRepository()

            for idx, notification in enumerate(notifications, start=1):
                # Получить событие
                event = None
                if notification.event_id not in events_cache:
                    try:
                        events_cache[notification.event_id] = self.event_repo.get_event(notification.event_id)
                    except:
                        events_cache[notification.event_id] = None
                event = events_cache[notification.event_id]

                # Получить человека и тип события
                person_name = "N/A"
                event_type_name = "N/A"

                if event:
                    # Получаем тип события по ID
                    if event.event_type_id:
                        try:
                            et = event_type_repo.get_by_id(event.event_type_id)
                            event_type_name = et.name if et else "N/A"
                        except:
                            event_type_name = "N/A"

                    # Получаем человека
                    if event.person_id not in persons_cache:
                        try:
                            persons_cache[event.person_id] = self.person_repo.get_person(event.person_id)
                        except:
                            persons_cache[event.person_id] = None

                    person = persons_cache.get(event.person_id)
                    if person:
                        person_name = f"{person.first_name} {person.last_name}"

                sent_time = notification.sent_at.strftime('%d.%m.%Y %H:%M') if notification.sent_at else 'N/A'

                # Иконка статуса
                status_icons = {'planned': '⏳', 'sent': '✓', 'failed': '✗'}
                status_icon = status_icons.get(notification.status, '?')
                status_text = f"{status_icon} {notification.status}"

                # Кнопка выбора
                select_btn = ctk.CTkButton(
                    self.table_frame,
                    text="◉",
                    width=40,
                    command=lambda n_id=notification.id, btn_idx=idx - 1: self.select_notification(n_id, btn_idx)
                )
                select_btn.grid(row=idx, column=0, padx=5, pady=2)
                self.notification_buttons.append(select_btn)

                # Остальные колонки
                values = [
                    str(notification.id),
                    event_type_name,
                    person_name,
                    sent_time,
                    status_text
                ]

                for col_idx, value in enumerate(values, start=1):
                    label = ctk.CTkLabel(self.table_frame, text=value)
                    label.grid(row=idx, column=col_idx, padx=10, pady=2, sticky="w")

            if not notifications:
                ctk.CTkLabel(
                    self.table_frame,
                    text="Žádná upozornění",
                    text_color="gray"
                ).grid(row=1, column=0, columnspan=6, pady=20)

        except Exception as e:
            ctk.CTkLabel(
                self.table_frame,
                text=f"Chyba načítání: {str(e)}",
                text_color="red"
            ).grid(row=1, column=0, columnspan=6, pady=20)
            import traceback
            traceback.print_exc()

    def select_notification(self, notification_id, button_index):
        """Выбрать уведомление"""
        self.selected_notification_id = notification_id

        for idx, btn in enumerate(self.notification_buttons):
            if idx == button_index:
                btn.configure(fg_color="green")
            else:
                btn.configure(fg_color=("gray75", "gray25"))

    def create_test_notification(self):
        """Создать тестовое уведомление"""
        # Получить первое событие
        events = self.event_repo.get_all_events()
        if not events:
            self.show_warning("Nejprve vytvořte alespoň jednu událost!")
            return

        event = events[0]

        # Создать уведомление
        notification = Notification(
            event_id=event.id,
            sent_at=datetime.now(),
            status='planned'
        )

        try:
            self.notification_repo.add_notification(notification)
            self.refresh()
        except Exception as e:
            self.show_warning(f"Chyba: {str(e)}")

    def resend_notification(self):
        """Повторно отправить уведомление"""
        if not self.selected_notification_id:
            self.show_warning("Vyberte prosím upozornění")
            return

        notification = self.notification_repo.get_notification(self.selected_notification_id)
        if not notification:
            return

        # Обновить статус на "sent" и время
        notification.status = 'sent'
        notification.sent_at = datetime.now()

        try:
            self.notification_repo.update_notification(notification)
            self.refresh()
        except Exception as e:
            self.show_warning(f"Chyba: {str(e)}")

    def delete_notification(self):
        """Удалить уведомление"""
        if not self.selected_notification_id:
            self.show_warning("Vyberte prosím upozornění")
            return

        # Диалог подтверждения
        confirm = ctk.CTkToplevel(self)
        confirm.title("Potvrdit smazání")
        confirm.geometry("400x150")
        confirm.resizable(False, False)
        confirm.transient(self)
        confirm.grab_set()

        ctk.CTkLabel(
            confirm,
            text=f"❓ Opravdu smazat upozornění ID: {self.selected_notification_id}?",
            font=ctk.CTkFont(size=14),
            justify="center"
        ).pack(padx=20, pady=30)

        btn_frame = ctk.CTkFrame(confirm, fg_color="transparent")
        btn_frame.pack(pady=10)

        def do_delete():
            try:
                self.notification_repo.delete_notification(self.selected_notification_id)
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
