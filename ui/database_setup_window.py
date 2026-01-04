import customtkinter as ctk
import pyodbc
from config import Config
import threading


class DatabaseSetupWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.success = False
        self.title("🔄 Inicializace databáze")
        self.geometry("700x500")
        self.resizable(False, False)

        # Центрирование
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.winfo_screenheight() // 2) - (500 // 2)
        self.geometry(f"700x500+{x}+{y}")

        self.transient(parent)
        self.grab_set()

        # Заголовок
        ctk.CTkLabel(
            self,
            text="🔄 Inicializace databáze",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(padx=30, pady=(30, 15))

        # Лог
        self.log_frame = ctk.CTkScrollableFrame(self, width=640, height=320)
        self.log_frame.pack(padx=30, pady=(0, 15))

        self.log_text = ctk.CTkTextbox(self.log_frame, width=620, height=300, font=ctk.CTkFont(size=12))
        self.log_text.pack(fill="both", expand=True)

        # Прогресс-бар
        self.progress = ctk.CTkProgressBar(self, width=640)
        self.progress.pack(padx=30, pady=(0, 15))
        self.progress.set(0)

        # Кнопка закрытия (вначале неактивна)
        self.close_btn = ctk.CTkButton(
            self,
            text="Zavřít",
            command=self.destroy,
            width=150,
            state="disabled"
        )
        self.close_btn.pack(pady=(0, 30))

        self.config = Config()

    def log(self, message, level="INFO"):
        """Добавить сообщение в лог"""
        colors = {
            "INFO": "",
            "SUCCESS": "🟢 ",
            "ERROR": "🔴 ",
            "WARNING": "🟡 "
        }
        prefix = colors.get(level, "")
        self.log_text.insert("end", f"{prefix}{message}\n")
        self.log_text.see("end")
        self.update()

    def run_initialization(self):
        """Запустить инициализацию в отдельном потоке"""
        thread = threading.Thread(target=self._initialize_database, daemon=True)
        thread.start()

    def _initialize_database(self):
        """Выполнить инициализацию БД"""
        self.log("Zahájení inicializace databáze...", "INFO")

        # SQL команды (разбиты по GO)
        sql_commands = self._get_sql_commands()

        total_commands = len(sql_commands)

        try:
            # Подключение
            conn_str = f'DRIVER={{{self.config.driver}}};SERVER={self.config.server};DATABASE={self.config.database};'
            if self.config.trusted_connection:
                conn_str += 'Trusted_Connection=yes;'

            self.log(f"Připojování k serveru: {self.config.server}", "INFO")
            self.log(f"Databáze: {self.config.database}", "INFO")

            conn = pyodbc.connect(conn_str, timeout=30)
            conn.autocommit = True
            cursor = conn.cursor()

            self.log("Připojení úspěšné!", "SUCCESS")

            # Выполнение команд
            executed = 0
            errors = 0

            for idx, cmd in enumerate(sql_commands, 1):
                try:
                    # Пропускаем пустые команды и комментарии
                    if not cmd.strip() or cmd.strip().startswith('--'):
                        continue

                    # Определяем тип команды
                    cmd_type = self._get_command_type(cmd)

                    self.log(f"[{idx}/{total_commands}] {cmd_type}...", "INFO")

                    cursor.execute(cmd)
                    executed += 1

                    # Обновление прогресс-бара
                    progress_value = idx / total_commands
                    self.progress.set(progress_value)

                except pyodbc.Error as e:
                    error_msg = str(e)
                    # Игнорируем ошибки "объект уже существует"
                    if "already exists" in error_msg or "již existuje" in error_msg:
                        self.log(f"  ⚠ Objekt již existuje, přeskakuji...", "WARNING")
                    else:
                        self.log(f"  ✗ Chyba: {error_msg[:100]}", "ERROR")
                        errors += 1

            cursor.close()
            conn.close()

            # Итоги
            self.log("\n" + "=" * 60, "INFO")
            self.log(f"Inicializace dokončena!", "SUCCESS")
            self.log(f"Úspěšně provedeno: {executed} příkazů", "SUCCESS")

            if errors > 0:
                self.log(f"Chyby: {errors}", "WARNING")
            else:
                self.log("Bez chyb! ✓", "SUCCESS")

            self.success = True

        except Exception as e:
            self.log("\n" + "=" * 60, "ERROR")
            self.log(f"Kritická chyba: {str(e)}", "ERROR")
            self.success = False

        finally:
            # Активация кнопки закрытия
            self.close_btn.configure(state="normal", fg_color="green")
            self.progress.set(1.0)

    def _get_sql_commands(self):
        """Получить список SQL команд, разбитых по GO"""
        sql_script = """
SET ANSI_NULLS ON
SET QUOTED_IDENTIFIER ON

-- Таблица типов событий
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[event_type]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[event_type](
    [id] [int] IDENTITY(1,1) NOT NULL,
    [name] [nvarchar](50) NOT NULL,
PRIMARY KEY CLUSTERED ([id] ASC),
UNIQUE NONCLUSTERED ([name] ASC)
)
END

-- Таблица персон
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[person]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[person](
    [id] [int] IDENTITY(1,1) NOT NULL,
    [first_name] [nvarchar](100) NOT NULL,
    [last_name] [nvarchar](100) NOT NULL,
    [birth_date] [date] NULL,
    [gender] [nvarchar](10) NULL,
    [is_active] [bit] NOT NULL DEFAULT 1,
    [created_at] [datetime2](7) NULL DEFAULT (getdate()),
PRIMARY KEY CLUSTERED ([id] ASC)
)
END

-- Таблица групп
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[group]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[group](
    [id] [int] IDENTITY(1,1) NOT NULL,
    [name] [nvarchar](100) NOT NULL,
    [created_at] [datetime2](7) NULL DEFAULT (getdate()),
PRIMARY KEY CLUSTERED ([id] ASC)
)
END

-- Таблица связи person-group
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[person_group]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[person_group](
    [person_id] [int] NOT NULL,
    [group_id] [int] NOT NULL,
    [added_at] [datetime2](7) NULL DEFAULT (getdate()),
PRIMARY KEY CLUSTERED ([person_id] ASC, [group_id] ASC)
)
END

-- Таблица событий
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[event]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[event](
    [id] [int] IDENTITY(1,1) NOT NULL,
    [person_id] [int] NOT NULL,
    [event_date] [date] NOT NULL,
    [reminder_days_before] [int] NOT NULL DEFAULT 7,
    [created_at] [datetime2](7) NULL DEFAULT (getdate()),
    [event_type_id] [int] NOT NULL,
    [reminder_time] [time](7) NULL,
PRIMARY KEY CLUSTERED ([id] ASC)
)
END

-- Таблица уведомлений
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[notification]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[notification](
    [id] [int] IDENTITY(1,1) NOT NULL,
    [event_id] [int] NOT NULL,
    [sent_at] [datetime2](7) NOT NULL DEFAULT (getdate()),
    [status] [nvarchar](20) NOT NULL,
PRIMARY KEY CLUSTERED ([id] ASC)
)
END

-- Таблица пользователей
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[user]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[user](
    [id] [int] IDENTITY(1,1) NOT NULL,
    [name] [nvarchar](100) NOT NULL,
    [email] [nvarchar](255) NOT NULL,
    [notifications_enabled] [bit] NOT NULL DEFAULT 1,
    [created_at] [datetime2](7) NULL DEFAULT (getdate()),
PRIMARY KEY CLUSTERED ([id] ASC),
UNIQUE NONCLUSTERED ([email] ASC)
)
END

-- Внешний ключ: event -> event_type
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_event_event_type]'))
BEGIN
ALTER TABLE [dbo].[event] WITH CHECK ADD CONSTRAINT [FK_event_event_type] FOREIGN KEY([event_type_id])
REFERENCES [dbo].[event_type] ([id])
END

-- Внешний ключ: event -> person
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_event_person]'))
BEGIN
ALTER TABLE [dbo].[event] WITH CHECK ADD CONSTRAINT [FK_event_person] FOREIGN KEY([person_id])
REFERENCES [dbo].[person] ([id]) ON DELETE CASCADE
END

-- Внешний ключ: notification -> event
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_notification_event]'))
BEGIN
ALTER TABLE [dbo].[notification] WITH CHECK ADD CONSTRAINT [FK_notification_event] FOREIGN KEY([event_id])
REFERENCES [dbo].[event] ([id]) ON DELETE CASCADE
END

-- Внешний ключ: person_group -> group
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_person_group_group]'))
BEGIN
ALTER TABLE [dbo].[person_group] WITH CHECK ADD CONSTRAINT [FK_person_group_group] FOREIGN KEY([group_id])
REFERENCES [dbo].[group] ([id]) ON DELETE CASCADE
END

-- Внешний ключ: person_group -> person
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_person_group_person]'))
BEGIN
ALTER TABLE [dbo].[person_group] WITH CHECK ADD CONSTRAINT [FK_person_group_person] FOREIGN KEY([person_id])
REFERENCES [dbo].[person] ([id]) ON DELETE CASCADE
END

-- Проверка: reminder_days_before >= 0
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE name = 'CK_event_reminder_days')
BEGIN
ALTER TABLE [dbo].[event] WITH CHECK ADD CONSTRAINT [CK_event_reminder_days] CHECK (([reminder_days_before]>=(0)))
END

-- Проверка: status в notification
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE name = 'CK_notification_status')
BEGIN
ALTER TABLE [dbo].[notification] WITH CHECK ADD CONSTRAINT [CK_notification_status] 
CHECK (([status]='failed' OR [status]='sent' OR [status]='planned'))
END

-- Проверка: gender в person
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE name = 'CK_person_gender')
BEGIN
ALTER TABLE [dbo].[person] WITH CHECK ADD CONSTRAINT [CK_person_gender]
CHECK (([gender]='other' OR [gender]='female' OR [gender]='male'))
END

-- View: upcoming events
IF EXISTS (SELECT * FROM sys.views WHERE name = 'v_upcoming_events')
DROP VIEW [dbo].[v_upcoming_events]

EXEC('CREATE VIEW [dbo].[v_upcoming_events] AS
SELECT
    e.id AS event_id,
    e.event_date,
    e.reminder_days_before,
    e.reminder_time,
    et.name AS event_type,
    p.id AS person_id,
    p.first_name,
    p.last_name,
    g.name AS group_name,
    DATEDIFF(day, GETDATE(), e.event_date) AS days_until_event
FROM event e
INNER JOIN person p ON e.person_id = p.id
INNER JOIN event_type et ON e.event_type_id = et.id
LEFT JOIN person_group pg ON p.id = pg.person_id
LEFT JOIN [group] g ON pg.group_id = g.id
WHERE e.event_date >= CAST(GETDATE() AS DATE)')

-- View: event summary
IF EXISTS (SELECT * FROM sys.views WHERE name = 'v_event_summary')
DROP VIEW [dbo].[v_event_summary]

EXEC('CREATE VIEW [dbo].[v_event_summary] AS
SELECT
    e.id AS event_id,
    e.event_date,
    e.reminder_days_before,
    e.reminder_time,
    et.name AS event_type,
    p.first_name + '' '' + p.last_name AS person_name,
    DATEDIFF(day, GETDATE(), e.event_date) AS days_until,
    CASE
        WHEN DATEDIFF(day, GETDATE(), e.event_date) < 0 THEN ''prošlé''
        WHEN DATEDIFF(day, GETDATE(), e.event_date) = 0 THEN ''dnes''
        WHEN DATEDIFF(day, GETDATE(), e.event_date) <= 7 THEN ''tento týden''
        WHEN DATEDIFF(day, GETDATE(), e.event_date) <= 30 THEN ''tento měsíc''
        ELSE ''budoucí''
    END AS time_category
FROM event e
INNER JOIN person p ON e.person_id = p.id
INNER JOIN event_type et ON e.event_type_id = et.id')

-- View: group statistics
IF EXISTS (SELECT * FROM sys.views WHERE name = 'v_group_statistics')
DROP VIEW [dbo].[v_group_statistics]

EXEC('CREATE VIEW [dbo].[v_group_statistics] AS
SELECT
    g.id AS group_id,
    g.name AS group_name,
    COUNT(DISTINCT pg.person_id) AS total_persons,
    COUNT(DISTINCT e.id) AS total_events
FROM [group] g
LEFT JOIN person_group pg ON g.id = pg.group_id
LEFT JOIN event e ON pg.person_id = e.person_id
GROUP BY g.id, g.name')
"""

        # Разбиваем по блокам BEGIN...END и отдельным командам
        commands = []
        current_block = []
        in_block = False

        for line in sql_script.split('\n'):
            line = line.strip()

            if not line or line.startswith('--'):
                continue

            if 'BEGIN' in line:
                in_block = True
                current_block.append(line)
            elif 'END' in line:
                current_block.append(line)
                commands.append('\n'.join(current_block))
                current_block = []
                in_block = False
            elif in_block:
                current_block.append(line)
            else:
                if line:
                    commands.append(line)

        return commands

    def _get_command_type(self, cmd):
        """Определить тип SQL команды для лога"""
        cmd_upper = cmd.upper()
        if 'CREATE TABLE' in cmd_upper:
            # Извлечь имя таблицы
            start = cmd_upper.find('CREATE TABLE') + 13
            end = cmd_upper.find('(', start)
            table_name = cmd[start:end].strip().replace('[DBO].', '').replace('[', '').replace(']', '')
            return f"Vytváření tabulky: {table_name}"
        elif 'CREATE VIEW' in cmd_upper:
            return "Vytváření view"
        elif 'ALTER TABLE' in cmd_upper and 'ADD CONSTRAINT' in cmd_upper:
            return "Přidávání omezení/cizího klíče"
        elif 'DROP VIEW' in cmd_upper:
            return "Mazání view"
        else:
            return "Provádění příkazu"


def show_database_setup():
    """
    Показать окно инициализации БД и вернуть результат
    Returns:
        bool: True если инициализация успешна, False если отменена или ошибка
    """
    # Создать временное окно
    root = ctk.CTk()
    root.withdraw()  # Скрыть главное окно

    # Диалог подтверждения
    dialog = ctk.CTkToplevel(root)
    dialog.title("Инициализация базы данных")
    dialog.geometry("550x300")
    dialog.resizable(False, False)

    # Центрирование
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (550 // 2)
    y = (dialog.winfo_screenheight() // 2) - (300 // 2)
    dialog.geometry(f"550x300+{x}+{y}")

    dialog.grab_set()

    result = {'proceed': False}

    # Заголовок
    ctk.CTkLabel(
        dialog,
        text="🗄️ Databáze nebyla nalezena",
        font=ctk.CTkFont(size=20, weight="bold")
    ).pack(padx=30, pady=(30, 15))

    # Текст
    ctk.CTkLabel(
        dialog,
        text="Aplikace nenašla existující databázi.\n\n"
             "Chcete vytvořit novou databázi?\n\n"
             "Budou vytvořeny všechny potřebné tabulky,\n"
             "view a vztahy.",
        justify="center",
        font=ctk.CTkFont(size=13)
    ).pack(padx=30, pady=(0, 20))

    def on_proceed():
        result['proceed'] = True
        dialog.destroy()

    def on_cancel():
        result['proceed'] = False
        dialog.destroy()

    # Кнопки
    btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
    btn_frame.pack(pady=(0, 30))

    ctk.CTkButton(
        btn_frame,
        text="❌ Zrušit",
        command=on_cancel,
        width=120,
        height=40,
        font=ctk.CTkFont(size=13),
        fg_color="gray50",
        hover_color="gray40"
    ).pack(side="left", padx=10)

    ctk.CTkButton(
        btn_frame,
        text="✅ Vytvořit databázi",
        command=on_proceed,
        width=150,
        height=40,
        font=ctk.CTkFont(size=13),
        fg_color="green",
        hover_color="darkgreen"
    ).pack(side="left", padx=10)

    dialog.protocol("WM_DELETE_WINDOW", on_cancel)

    # Ждать выбора пользователя
    root.wait_window(dialog)

    if not result['proceed']:
        root.destroy()
        return False

    # Запустить окно инициализации
    setup_window = DatabaseSetupWindow(root)
    setup_window.run_initialization()

    # Ждать закрытия окна
    root.wait_window(setup_window)

    success = setup_window.success
    root.destroy()

    return success
