GO
/****** Object:  Table [dbo].[event_type]    Script Date: 04.01.2026 22:50:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[event_type](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](50) NOT NULL,
PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED
(
	[name] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[person]    Script Date: 04.01.2026 22:50:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
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
GO
/****** Object:  Table [dbo].[group]    Script Date: 04.01.2026 22:50:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[group](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](100) NOT NULL,
	[created_at] [datetime2](7) NULL,
PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[person_group]    Script Date: 04.01.2026 22:50:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
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
GO
/****** Object:  Table [dbo].[event]    Script Date: 04.01.2026 22:50:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
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
GO
/****** Object:  View [dbo].[v_upcoming_events]    Script Date: 04.01.2026 22:50:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
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
WHERE e.event_date >= CAST(GETDATE() AS DATE);

GO
/****** Object:  View [dbo].[v_event_summary]    Script Date: 04.01.2026 22:50:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[v_event_summary] AS
SELECT
    e.id AS event_id,
    e.event_date,
    e.reminder_days_before,
    e.reminder_time,
    et.name AS event_type,
    p.first_name + ' ' + p.last_name AS person_name,
    DATEDIFF(day, GETDATE(), e.event_date) AS days_until,
    CASE
        WHEN DATEDIFF(day, GETDATE(), e.event_date) < 0 THEN 'prošlé'
        WHEN DATEDIFF(day, GETDATE(), e.event_date) = 0 THEN 'dnes'
        WHEN DATEDIFF(day, GETDATE(), e.event_date) <= 7 THEN 'tento týden'
        WHEN DATEDIFF(day, GETDATE(), e.event_date) <= 30 THEN 'tento měsíc'
        ELSE 'budoucí'
    END AS time_category
FROM event e
INNER JOIN person p ON e.person_id = p.id
INNER JOIN event_type et ON e.event_type_id = et.id;

GO
/****** Object:  View [dbo].[v_group_statistics]    Script Date: 04.01.2026 22:50:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[v_group_statistics] AS
SELECT
    g.id AS group_id,
    g.name AS group_name,
    COUNT(DISTINCT pg.person_id) AS total_persons,
    COUNT(DISTINCT e.id) AS total_events
FROM [group] g
LEFT JOIN person_group pg ON g.id = pg.group_id
LEFT JOIN event e ON pg.person_id = e.person_id
GROUP BY g.id, g.name;

GO
/****** Object:  Table [dbo].[notification]    Script Date: 04.01.2026 22:50:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
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
GO
/****** Object:  Table [dbo].[user]    Script Date: 04.01.2026 22:50:36 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[user](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](100) NOT NULL,
	[email] [nvarchar](255) NOT NULL,
	[notifications_enabled] [bit] NOT NULL,
	[created_at] [datetime2](7) NULL,
PRIMARY KEY CLUSTERED
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED
(
	[email] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[event] ADD  DEFAULT ((7)) FOR [reminder_days_before]
GO
ALTER TABLE [dbo].[event] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[group] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[notification] ADD  DEFAULT (getdate()) FOR [sent_at]
GO
ALTER TABLE [dbo].[person] ADD  DEFAULT ((1)) FOR [is_active]
GO
ALTER TABLE [dbo].[person] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[person_group] ADD  DEFAULT (getdate()) FOR [added_at]
GO
ALTER TABLE [dbo].[user] ADD  DEFAULT ((1)) FOR [notifications_enabled]
GO
ALTER TABLE [dbo].[user] ADD  DEFAULT (getdate()) FOR [created_at]
GO
ALTER TABLE [dbo].[event]  WITH CHECK ADD  CONSTRAINT [FK_event_event_type] FOREIGN KEY([event_type_id])
REFERENCES [dbo].[event_type] ([id])
GO
ALTER TABLE [dbo].[event] CHECK CONSTRAINT [FK_event_event_type]
GO
ALTER TABLE [dbo].[event]  WITH CHECK ADD  CONSTRAINT [FK_event_person] FOREIGN KEY([person_id])
REFERENCES [dbo].[person] ([id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[event] CHECK CONSTRAINT [FK_event_person]
GO
ALTER TABLE [dbo].[notification]  WITH CHECK ADD  CONSTRAINT [FK_notification_event] FOREIGN KEY([event_id])
REFERENCES [dbo].[event] ([id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[notification] CHECK CONSTRAINT [FK_notification_event]
GO
ALTER TABLE [dbo].[person_group]  WITH CHECK ADD  CONSTRAINT [FK_person_group_group] FOREIGN KEY([group_id])
REFERENCES [dbo].[group] ([id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[person_group] CHECK CONSTRAINT [FK_person_group_group]
GO
ALTER TABLE [dbo].[person_group]  WITH CHECK ADD  CONSTRAINT [FK_person_group_person] FOREIGN KEY([person_id])
REFERENCES [dbo].[person] ([id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[person_group] CHECK CONSTRAINT [FK_person_group_person]
GO
ALTER TABLE [dbo].[event]  WITH CHECK ADD CHECK  (([reminder_days_before]>=(0)))
GO
ALTER TABLE [dbo].[event]  WITH CHECK ADD CHECK  (([reminder_days_before]>=(0)))
GO
ALTER TABLE [dbo].[notification]  WITH CHECK ADD CHECK  (([status]='failed' OR [status]='sent' OR [status]='planned'))
GO
ALTER TABLE [dbo].[notification]  WITH CHECK ADD CHECK  (([status]='failed' OR [status]='sent' OR [status]='planned'))
GO
ALTER TABLE [dbo].[person]  WITH CHECK ADD CHECK  (([gender]='other' OR [gender]='female' OR [gender]='male'))
GO
ALTER TABLE [dbo].[person]  WITH CHECK ADD CHECK  (([gender]='other' OR [gender]='female' OR [gender]='male'))
GO
