import pyodbc
from config import Config


class DatabaseDeployer:
    """Класс для развёртывания БД из SQL скрипта"""

    def __init__(self):
        self.config = Config()

    def check_database_exists(self):
        """Проверить существование БД"""
        try:
            # Подключиться к master для проверки
            master_conn_str = f'DRIVER={{{self.config.driver}}};SERVER={self.config.server};DATABASE=master;'
            if self.config.trusted_connection:
                master_conn_str += 'Trusted_Connection=yes;'

            conn = pyodbc.connect(master_conn_str, timeout=10)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT database_id FROM sys.databases WHERE name = ?",
                (self.config.database,)
            )
            exists = cursor.fetchone() is not None

            cursor.close()
            conn.close()

            return exists

        except Exception as e:
            print(f"⚠️ Ошибка проверки БД: {e}")
            return False

    def deploy_database(self):
        """
        Развернуть БД из SQL скрипта
        Возвращает (success: bool, message: str)
        """
        try:
            print("🚀 Начало развёртывания базы данных...")

            # ===== ВСТАВЬ СЮДА СВОЙ SQL СКРИПТ =====
            sql_script = """
USE master;
GO

CREATE DATABASE [Contact_Event_Reminder_System];
GO

USE [Contact_Event_Reminder_System];
GO

/****** Object:  Table [dbo].[event_type]    Script Date: 11.01.2026 15:45:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[event_type]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[event_type](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](50) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
END
GO
/****** Object:  Table [dbo].[person]    Script Date: 11.01.2026 15:45:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[person]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[person](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[first_name] [nvarchar](100) NOT NULL,
	[last_name] [nvarchar](100) NOT NULL,
	[birth_date] [date] NULL,
	[gender] [nvarchar](10) NULL,
	[is_active] [bit] NOT NULL,
	[created_at] [datetime2](7) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
END
GO
/****** Object:  Table [dbo].[group]    Script Date: 11.01.2026 15:45:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[group]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[group](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](100) NOT NULL,
	[created_at] [datetime2](7) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
END
GO
/****** Object:  Table [dbo].[person_group]    Script Date: 11.01.2026 15:45:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[person_group]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[person_group](
	[person_id] [int] NOT NULL,
	[group_id] [int] NOT NULL,
	[added_at] [datetime2](7) NULL,
PRIMARY KEY CLUSTERED 
(
	[person_id] ASC,
	[group_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
END
GO
/****** Object:  Table [dbo].[event]    Script Date: 11.01.2026 15:45:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[event]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[event](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[person_id] [int] NOT NULL,
	[event_date] [date] NOT NULL,
	[reminder_days_before] [int] NOT NULL,
	[created_at] [datetime2](7) NULL,
	[event_type_id] [int] NOT NULL,
	[reminder_time] [time](7) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
END
GO
/****** Object:  View [dbo].[v_upcoming_events]    Script Date: 11.01.2026 15:45:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.views WHERE object_id = OBJECT_ID(N'[dbo].[v_upcoming_events]'))
EXEC dbo.sp_executesql @statement = N'
    CREATE VIEW [dbo].[v_upcoming_events] AS
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
    WHERE e.event_date >= CAST(GETDATE() AS DATE)
        ' 
GO
/****** Object:  View [dbo].[v_event_summary]    Script Date: 11.01.2026 15:45:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.views WHERE object_id = OBJECT_ID(N'[dbo].[v_event_summary]'))
EXEC dbo.sp_executesql @statement = N'
    CREATE VIEW [dbo].[v_event_summary] AS
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
    INNER JOIN event_type et ON e.event_type_id = et.id
        ' 
GO
/****** Object:  View [dbo].[v_group_statistics]    Script Date: 11.01.2026 15:45:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.views WHERE object_id = OBJECT_ID(N'[dbo].[v_group_statistics]'))
EXEC dbo.sp_executesql @statement = N'
    CREATE VIEW [dbo].[v_group_statistics] AS
    SELECT
        g.id AS group_id,
        g.name AS group_name,
        COUNT(DISTINCT pg.person_id) AS total_persons,
        COUNT(DISTINCT e.id) AS total_events
    FROM [group] g
    LEFT JOIN person_group pg ON g.id = pg.group_id
    LEFT JOIN event e ON pg.person_id = e.person_id
    GROUP BY g.id, g.name
        ' 
GO
/****** Object:  Table [dbo].[notification]    Script Date: 11.01.2026 15:45:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[notification]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[notification](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[event_id] [int] NOT NULL,
	[sent_at] [datetime2](7) NOT NULL,
	[status] [nvarchar](20) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
END
GO
/****** Object:  Table [dbo].[user]    Script Date: 11.01.2026 15:45:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[user]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[user](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](100) NOT NULL,
	[email] [nvarchar](255) NOT NULL,
	[notifications_enabled] [bit] NOT NULL,
	[created_at] [datetime2](7) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
END
GO
SET IDENTITY_INSERT [dbo].[event] ON 

INSERT [dbo].[event] ([id], [person_id], [event_date], [reminder_days_before], [created_at], [event_type_id], [reminder_time]) VALUES (5, 12, CAST(N'2026-01-07' AS Date), 7, CAST(N'2026-01-05T00:37:06.5800000' AS DateTime2), 1, CAST(N'09:00:00' AS Time))
INSERT [dbo].[event] ([id], [person_id], [event_date], [reminder_days_before], [created_at], [event_type_id], [reminder_time]) VALUES (6, 12, CAST(N'2026-01-06' AS Date), 1, CAST(N'2026-01-05T00:49:02.6666667' AS DateTime2), 4, CAST(N'09:00:00' AS Time))
SET IDENTITY_INSERT [dbo].[event] OFF
GO
SET IDENTITY_INSERT [dbo].[event_type] ON 

INSERT [dbo].[event_type] ([id], [name]) VALUES (2, N'anniversary')
INSERT [dbo].[event_type] ([id], [name]) VALUES (1, N'birthday')
INSERT [dbo].[event_type] ([id], [name]) VALUES (4, N'daily scrum')
INSERT [dbo].[event_type] ([id], [name]) VALUES (3, N'other')
SET IDENTITY_INSERT [dbo].[event_type] OFF
GO
SET IDENTITY_INSERT [dbo].[group] ON 

INSERT [dbo].[group] ([id], [name], [created_at]) VALUES (9, N'rodina', CAST(N'2026-01-05T00:34:01.1833333' AS DateTime2))
SET IDENTITY_INSERT [dbo].[group] OFF
GO
SET IDENTITY_INSERT [dbo].[notification] ON 

INSERT [dbo].[notification] ([id], [event_id], [sent_at], [status]) VALUES (4, 5, CAST(N'2026-01-05T00:37:25.7232980' AS DateTime2), N'sent')
INSERT [dbo].[notification] ([id], [event_id], [sent_at], [status]) VALUES (5, 5, CAST(N'2026-01-05T00:37:23.0842780' AS DateTime2), N'planned')
INSERT [dbo].[notification] ([id], [event_id], [sent_at], [status]) VALUES (6, 6, CAST(N'2026-01-05T00:51:12.6233333' AS DateTime2), N'sent')
INSERT [dbo].[notification] ([id], [event_id], [sent_at], [status]) VALUES (7, 6, CAST(N'2026-01-05T00:51:13.5366667' AS DateTime2), N'sent')
SET IDENTITY_INSERT [dbo].[notification] OFF
GO
SET IDENTITY_INSERT [dbo].[person] ON 

INSERT [dbo].[person] ([id], [first_name], [last_name], [birth_date], [gender], [is_active], [created_at]) VALUES (12, N'maxim', N'mazuret', CAST(N'2001-02-01' AS Date), N'male', 1, CAST(N'2026-01-05T00:33:48.0800000' AS DateTime2))
SET IDENTITY_INSERT [dbo].[person] OFF
GO
INSERT [dbo].[person_group] ([person_id], [group_id], [added_at]) VALUES (12, 9, CAST(N'2026-01-05T00:34:06.6500000' AS DateTime2))
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [UQ__event_ty__72E12F1B3394CDF9]    Script Date: 11.01.2026 15:45:53 ******/
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'[dbo].[event_type]') AND name = N'UQ__event_ty__72E12F1B3394CDF9')
ALTER TABLE [dbo].[event_type] ADD UNIQUE NONCLUSTERED 
(
	[name] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [UQ__user__AB6E61645F713DF5]    Script Date: 11.01.2026 15:45:53 ******/
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'[dbo].[user]') AND name = N'UQ__user__AB6E61645F713DF5')
ALTER TABLE [dbo].[user] ADD UNIQUE NONCLUSTERED 
(
	[email] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DF__event__reminder___6EF57B66]') AND type = 'D')
BEGIN
ALTER TABLE [dbo].[event] ADD  DEFAULT ((7)) FOR [reminder_days_before]
END
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DF__event__created_a__70DDC3D8]') AND type = 'D')
BEGIN
ALTER TABLE [dbo].[event] ADD  DEFAULT (getdate()) FOR [created_at]
END
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DF__group__created_a__66603565]') AND type = 'D')
BEGIN
ALTER TABLE [dbo].[group] ADD  DEFAULT (getdate()) FOR [created_at]
END
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DF__notificat__sent___74AE54BC]') AND type = 'D')
BEGIN
ALTER TABLE [dbo].[notification] ADD  DEFAULT (getdate()) FOR [sent_at]
END
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DF__person__is_activ__628FA481]') AND type = 'D')
BEGIN
ALTER TABLE [dbo].[person] ADD  DEFAULT ((1)) FOR [is_active]
END
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DF__person__created___6383C8BA]') AND type = 'D')
BEGIN
ALTER TABLE [dbo].[person] ADD  DEFAULT (getdate()) FOR [created_at]
END
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DF__person_gr__added__693CA210]') AND type = 'D')
BEGIN
ALTER TABLE [dbo].[person_group] ADD  DEFAULT (getdate()) FOR [added_at]
END
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DF__user__notificati__5DCAEF64]') AND type = 'D')
BEGIN
ALTER TABLE [dbo].[user] ADD  DEFAULT ((1)) FOR [notifications_enabled]
END
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DF__user__created_at__5EBF139D]') AND type = 'D')
BEGIN
ALTER TABLE [dbo].[user] ADD  DEFAULT (getdate()) FOR [created_at]
END
GO
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_event_event_type]') AND parent_object_id = OBJECT_ID(N'[dbo].[event]'))
ALTER TABLE [dbo].[event]  WITH CHECK ADD  CONSTRAINT [FK_event_event_type] FOREIGN KEY([event_type_id])
REFERENCES [dbo].[event_type] ([id])
GO
IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_event_event_type]') AND parent_object_id = OBJECT_ID(N'[dbo].[event]'))
ALTER TABLE [dbo].[event] CHECK CONSTRAINT [FK_event_event_type]
GO
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_event_person]') AND parent_object_id = OBJECT_ID(N'[dbo].[event]'))
ALTER TABLE [dbo].[event]  WITH CHECK ADD  CONSTRAINT [FK_event_person] FOREIGN KEY([person_id])
REFERENCES [dbo].[person] ([id])
ON DELETE CASCADE
GO
IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_event_person]') AND parent_object_id = OBJECT_ID(N'[dbo].[event]'))
ALTER TABLE [dbo].[event] CHECK CONSTRAINT [FK_event_person]
GO
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_notification_event]') AND parent_object_id = OBJECT_ID(N'[dbo].[notification]'))
ALTER TABLE [dbo].[notification]  WITH CHECK ADD  CONSTRAINT [FK_notification_event] FOREIGN KEY([event_id])
REFERENCES [dbo].[event] ([id])
ON DELETE CASCADE
GO
IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_notification_event]') AND parent_object_id = OBJECT_ID(N'[dbo].[notification]'))
ALTER TABLE [dbo].[notification] CHECK CONSTRAINT [FK_notification_event]
GO
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_person_group_group]') AND parent_object_id = OBJECT_ID(N'[dbo].[person_group]'))
ALTER TABLE [dbo].[person_group]  WITH CHECK ADD  CONSTRAINT [FK_person_group_group] FOREIGN KEY([group_id])
REFERENCES [dbo].[group] ([id])
ON DELETE CASCADE
GO
IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_person_group_group]') AND parent_object_id = OBJECT_ID(N'[dbo].[person_group]'))
ALTER TABLE [dbo].[person_group] CHECK CONSTRAINT [FK_person_group_group]
GO
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_person_group_person]') AND parent_object_id = OBJECT_ID(N'[dbo].[person_group]'))
ALTER TABLE [dbo].[person_group]  WITH CHECK ADD  CONSTRAINT [FK_person_group_person] FOREIGN KEY([person_id])
REFERENCES [dbo].[person] ([id])
ON DELETE CASCADE
GO
IF  EXISTS (SELECT * FROM sys.foreign_keys WHERE object_id = OBJECT_ID(N'[dbo].[FK_person_group_person]') AND parent_object_id = OBJECT_ID(N'[dbo].[person_group]'))
ALTER TABLE [dbo].[person_group] CHECK CONSTRAINT [FK_person_group_person]
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK__event__reminder___3493CFA7]') AND parent_object_id = OBJECT_ID(N'[dbo].[event]'))
ALTER TABLE [dbo].[event]  WITH CHECK ADD CHECK  (([reminder_days_before]>=(0)))
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK__event__reminder___40F9A68C]') AND parent_object_id = OBJECT_ID(N'[dbo].[event]'))
ALTER TABLE [dbo].[event]  WITH CHECK ADD CHECK  (([reminder_days_before]>=(0)))
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK__event__reminder___41EDCAC5]') AND parent_object_id = OBJECT_ID(N'[dbo].[event]'))
ALTER TABLE [dbo].[event]  WITH CHECK ADD CHECK  (([reminder_days_before]>=(0)))
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK__event__reminder___503BEA1C]') AND parent_object_id = OBJECT_ID(N'[dbo].[event]'))
ALTER TABLE [dbo].[event]  WITH CHECK ADD CHECK  (([reminder_days_before]>=(0)))
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK__event__reminder___51300E55]') AND parent_object_id = OBJECT_ID(N'[dbo].[event]'))
ALTER TABLE [dbo].[event]  WITH CHECK ADD CHECK  (([reminder_days_before]>=(0)))
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK__event__reminder___6FE99F9F]') AND parent_object_id = OBJECT_ID(N'[dbo].[event]'))
ALTER TABLE [dbo].[event]  WITH CHECK ADD CHECK  (([reminder_days_before]>=(0)))
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK_event_reminder_days]') AND parent_object_id = OBJECT_ID(N'[dbo].[event]'))
ALTER TABLE [dbo].[event]  WITH CHECK ADD  CONSTRAINT [CK_event_reminder_days] CHECK  (([reminder_days_before]>=(0)))
GO
IF  EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK_event_reminder_days]') AND parent_object_id = OBJECT_ID(N'[dbo].[event]'))
ALTER TABLE [dbo].[event] CHECK CONSTRAINT [CK_event_reminder_days]
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK__notificat__statu__3587F3E0]') AND parent_object_id = OBJECT_ID(N'[dbo].[notification]'))
ALTER TABLE [dbo].[notification]  WITH CHECK ADD CHECK  (([status]='failed' OR [status]='sent' OR [status]='planned'))
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK__notificat__statu__42E1EEFE]') AND parent_object_id = OBJECT_ID(N'[dbo].[notification]'))
ALTER TABLE [dbo].[notification]  WITH CHECK ADD CHECK  (([status]='failed' OR [status]='sent' OR [status]='planned'))
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK__notificat__statu__43D61337]') AND parent_object_id = OBJECT_ID(N'[dbo].[notification]'))
ALTER TABLE [dbo].[notification]  WITH CHECK ADD CHECK  (([status]='failed' OR [status]='sent' OR [status]='planned'))
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK__notificat__statu__5224328E]') AND parent_object_id = OBJECT_ID(N'[dbo].[notification]'))
ALTER TABLE [dbo].[notification]  WITH CHECK ADD CHECK  (([status]='failed' OR [status]='sent' OR [status]='planned'))
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK__notificat__statu__531856C7]') AND parent_object_id = OBJECT_ID(N'[dbo].[notification]'))
ALTER TABLE [dbo].[notification]  WITH CHECK ADD CHECK  (([status]='failed' OR [status]='sent' OR [status]='planned'))
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK__notificat__statu__75A278F5]') AND parent_object_id = OBJECT_ID(N'[dbo].[notification]'))
ALTER TABLE [dbo].[notification]  WITH CHECK ADD CHECK  (([status]='failed' OR [status]='sent' OR [status]='planned'))
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK_notification_status]') AND parent_object_id = OBJECT_ID(N'[dbo].[notification]'))
ALTER TABLE [dbo].[notification]  WITH CHECK ADD  CONSTRAINT [CK_notification_status] CHECK  (([status]='failed' OR [status]='sent' OR [status]='planned'))
GO
IF  EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK_notification_status]') AND parent_object_id = OBJECT_ID(N'[dbo].[notification]'))
ALTER TABLE [dbo].[notification] CHECK CONSTRAINT [CK_notification_status]
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK__person__gender__367C1819]') AND parent_object_id = OBJECT_ID(N'[dbo].[person]'))
ALTER TABLE [dbo].[person]  WITH CHECK ADD CHECK  (([gender]='other' OR [gender]='female' OR [gender]='male'))
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK__person__gender__44CA3770]') AND parent_object_id = OBJECT_ID(N'[dbo].[person]'))
ALTER TABLE [dbo].[person]  WITH CHECK ADD CHECK  (([gender]='other' OR [gender]='female' OR [gender]='male'))
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK__person__gender__45BE5BA9]') AND parent_object_id = OBJECT_ID(N'[dbo].[person]'))
ALTER TABLE [dbo].[person]  WITH CHECK ADD CHECK  (([gender]='other' OR [gender]='female' OR [gender]='male'))
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK__person__gender__540C7B00]') AND parent_object_id = OBJECT_ID(N'[dbo].[person]'))
ALTER TABLE [dbo].[person]  WITH CHECK ADD CHECK  (([gender]='other' OR [gender]='female' OR [gender]='male'))
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK__person__gender__55009F39]') AND parent_object_id = OBJECT_ID(N'[dbo].[person]'))
ALTER TABLE [dbo].[person]  WITH CHECK ADD CHECK  (([gender]='other' OR [gender]='female' OR [gender]='male'))
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK__person__gender__619B8048]') AND parent_object_id = OBJECT_ID(N'[dbo].[person]'))
ALTER TABLE [dbo].[person]  WITH CHECK ADD CHECK  (([gender]='other' OR [gender]='female' OR [gender]='male'))
GO
IF NOT EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK_person_gender]') AND parent_object_id = OBJECT_ID(N'[dbo].[person]'))
ALTER TABLE [dbo].[person]  WITH CHECK ADD  CONSTRAINT [CK_person_gender] CHECK  (([gender]='other' OR [gender]='female' OR [gender]='male'))
GO
IF  EXISTS (SELECT * FROM sys.check_constraints WHERE object_id = OBJECT_ID(N'[dbo].[CK_person_gender]') AND parent_object_id = OBJECT_ID(N'[dbo].[person]'))
ALTER TABLE [dbo].[person] CHECK CONSTRAINT [CK_person_gender]
GO
"""
            # ========================================

            # Разделить скрипт на команды
            # Убираем USE master и CREATE DATABASE - будем делать отдельно

            # Шаг 1: Создать БД
            if not self._create_database():
                return False, "Ошибка создания базы данных"

            # Шаг 2: Выполнить остальной скрипт
            if not self._execute_schema_script(sql_script):
                return False, "Ошибка создания структуры БД"

            print("✅ База данных успешно развёрнута!")
            return True, "База данных успешно создана"

        except Exception as e:
            error_msg = f"Ошибка развёртывания БД: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg

    def _create_database(self):
        """Создать базу данных"""
        try:
            # Подключение к master
            master_conn_str = f'DRIVER={{{self.config.driver}}};SERVER={self.config.server};DATABASE=master;'
            if self.config.trusted_connection:
                master_conn_str += 'Trusted_Connection=yes;'

            conn = pyodbc.connect(master_conn_str, timeout=30)
            conn.autocommit = True
            cursor = conn.cursor()

            # Проверить существование
            cursor.execute(
                "SELECT database_id FROM sys.databases WHERE name = ?",
                (self.config.database,)
            )

            if cursor.fetchone() is not None:
                print(f"✅ База данных [{self.config.database}] уже существует")
                cursor.close()
                conn.close()
                return True

            # Создать БД
            print(f"🔨 Создание базы данных [{self.config.database}]...")
            cursor.execute(f"CREATE DATABASE [{self.config.database}]")
            print(f"✅ База данных [{self.config.database}] создана")

            cursor.close()
            conn.close()
            return True

        except Exception as e:
            print(f"❌ Ошибка создания БД: {e}")
            return False

    def _execute_schema_script(self, sql_script):
        """Выполнить SQL скрипт создания структуры"""
        try:
            # Подключение к созданной БД
            conn_str = f'DRIVER={{{self.config.driver}}};SERVER={self.config.server};DATABASE={self.config.database};'
            if self.config.trusted_connection:
                conn_str += 'Trusted_Connection=yes;'

            conn = pyodbc.connect(conn_str, timeout=60)
            conn.autocommit = True
            cursor = conn.cursor()

            print(f"🔧 Выполнение SQL скрипта...")

            # Убрать USE master и CREATE DATABASE из скрипта
            script = sql_script.replace('USE master;', '')
            script = script.replace('GO', '')
            script = script.replace('CREATE DATABASE [Contact_Event_Reminder_System];', '')
            script = script.replace('USE [Contact_Event_Reminder_System];', '')

            # Разделить на батчи по IF NOT EXISTS
            batches = self._split_sql_script(script)

            executed = 0
            for batch in batches:
                if batch.strip():
                    try:
                        cursor.execute(batch)
                        executed += 1
                    except pyodbc.Error as e:
                        # Игнорировать ошибки "уже существует"
                        error_msg = str(e).lower()
                        if 'already exist' in error_msg or 'уже существует' in error_msg:
                            print(f"  ⚠️ Объект уже существует, пропуск...")
                        else:
                            print(f"  ❌ Ошибка: {str(e)[:100]}")

            print(f"✅ Выполнено команд: {executed}")

            cursor.close()
            conn.close()
            return True

        except Exception as e:
            print(f"❌ Ошибка выполнения скрипта: {e}")
            return False

    def _split_sql_script(self, script):
        """Разделить SQL скрипт на батчи"""
        # Простое разделение по SET ANSI_NULLS ON
        batches = []
        current_batch = ""

        for line in script.split('\n'):
            current_batch += line + '\n'

            # Разделять по SET ANSI_NULLS для каждого объекта
            if 'SET ANSI_NULLS ON' in line and current_batch.strip():
                if len(current_batch.strip()) > 50:
                    batches.append(current_batch)
                    current_batch = ""

        if current_batch.strip():
            batches.append(current_batch)

        # Если батчей нет, вернуть весь скрипт одним куском
        if not batches:
            batches = [script]

        return batches
