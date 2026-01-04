import customtkinter as ctk


class ReminderNotificationWindow(ctk.CTkToplevel):
    def __init__(self, parent, reminders, notification_service):
        super().__init__(parent)

        self.reminders = reminders
        self.notification_service = notification_service

        self.title("🔔 Připomínky")
        self.geometry("600x500")
        self.resizable(False, False)

        # Центрирование
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.winfo_screenheight() // 2) - (500 // 2)
        self.geometry(f"600x500+{x}+{y}")

        # Поверх всех окон
        self.attributes('-topmost', True)
        self.lift()
        self.focus_force()

        self.create_widgets()

    def create_widgets(self):
        # Заголовок
        header = ctk.CTkFrame(self, fg_color="#1f538d", height=80)
        header.pack(fill="x", padx=0, pady=0)

        ctk.CTkLabel(
            header,
            text="🔔 Připomínky",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        ).pack(pady=20)

        # Счётчик
        count_text = f"Máte {len(self.reminders)} nadcházejících událostí"
        ctk.CTkLabel(
            self,
            text=count_text,
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack(pady=(20, 10))

        # Список напоминаний
        scrollable_frame = ctk.CTkScrollableFrame(self, width=560, height=300)
        scrollable_frame.pack(padx=20, pady=(0, 20))

        for reminder in self.reminders:
            self.create_reminder_card(scrollable_frame, reminder)

        # Кнопки
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))

        ctk.CTkButton(
            btn_frame,
            text="✅ Potvrdit a zavřít",
            command=self.confirm_and_close,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="green",
            hover_color="darkgreen"
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="⏰ Připomenout později",
            command=self.destroy,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="gray50",
            hover_color="gray40"
        ).pack(side="left", padx=10)

    def create_reminder_card(self, parent, reminder):
        """Создать карточку напоминания"""
        card = ctk.CTkFrame(parent, fg_color="#2b2b2b", corner_radius=10)
        card.pack(fill="x", padx=10, pady=8)

        # Иконка в зависимости от срочности
        days_until = reminder['days_until']
        if days_until == 0:
            icon = "🎉"
            color = "#ff6b6b"
        elif days_until == 1:
            icon = "⏰"
            color = "#ffa500"
        elif days_until <= 3:
            icon = "📅"
            color = "#4ecdc4"
        else:
            icon = "📆"
            color = "#95a5a6"

        # Заголовок
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            header_frame,
            text=icon,
            font=ctk.CTkFont(size=24)
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            header_frame,
            text=f"{reminder['first_name']} {reminder['last_name']}",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        ).pack(side="left", fill="x", expand=True)

        # Детали
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.pack(fill="x", padx=15, pady=(0, 5))

        event_date = reminder['event_date'].strftime('%d.%m.%Y')

        ctk.CTkLabel(
            details_frame,
            text=f"📌 {reminder['event_type']}",
            font=ctk.CTkFont(size=13),
            text_color="lightblue",
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            details_frame,
            text=f"📅 Datum: {event_date}",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w"
        ).pack(anchor="w")

        # Срочность
        if days_until == 0:
            urgency_text = "DNES!"
        elif days_until == 1:
            urgency_text = "ZÍTRA!"
        else:
            urgency_text = f"Za {days_until} dní"

        urgency_label = ctk.CTkLabel(
            details_frame,
            text=urgency_text,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=color,
            anchor="w"
        )
        urgency_label.pack(anchor="w", pady=(5, 10))

    def confirm_and_close(self):
        """Подтвердить и закрыть - отметить все как прочитанные"""
        for reminder in self.reminders:
            self.notification_service.mark_notification_sent(reminder['event_id'])

        self.destroy()
