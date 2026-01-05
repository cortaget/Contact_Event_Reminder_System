"""
Скрипт для сборки EXE файла
Запуск: python build_exe.py
"""
import PyInstaller.__main__
import os
import shutil

print("="*60)
print("🔨 СБОРКА EVENT REMINDER SYSTEM")
print("="*60)

# Получить путь к customtkinter
try:
    import customtkinter
    ctk_path = os.path.dirname(customtkinter.__file__)
    print(f"✅ CustomTkinter найден: {ctk_path}")
except ImportError:
    print("❌ CustomTkinter не установлен!")
    exit(1)

# Очистить старые сборки
if os.path.exists('build'):
    shutil.rmtree('build')
    print("🗑️  Удалена папка build/")

if os.path.exists('dist'):
    shutil.rmtree('dist')
    print("🗑️  Удалена папка dist/")

print("\n🔧 Запуск PyInstaller...")

# Запуск PyInstaller
PyInstaller.__main__.run([
    'main.py',                              # Главный файл
    '--name=Event_Reminder_System',         # Имя EXE
    '--onefile',                            # Один файл
    '--windowed',                           # Без консоли
    '--clean',                              # Очистить кеш

    # Скрытые импорты
    '--hidden-import=pyodbc',
    '--hidden-import=customtkinter',
    '--hidden-import=PIL',
    '--hidden-import=PIL._tkinter_finder',
    '--hidden-import=babel.numbers',

    # Добавить customtkinter данные
    f'--add-data={ctk_path};customtkinter/',

    # Исключить ненужные модули (уменьшить размер)
    '--exclude-module=matplotlib',
    '--exclude-module=numpy',
    '--exclude-module=pandas',
    '--exclude-module=scipy',
    '--exclude-module=pytest',

    # Логирование
    '--log-level=INFO',
])

print("\n" + "="*60)
print("✅ СБОРКА ЗАВЕРШЕНА!")
print("="*60)

# Проверить наличие EXE
exe_path = os.path.join('dist', 'Event_Reminder_System.exe')
if os.path.exists(exe_path):
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"📦 EXE файл: {exe_path}")
    print(f"📊 Размер: {size_mb:.1f} МБ")

    # Скопировать config.json рядом с EXE (если есть)
    if os.path.exists('config.json'):
        shutil.copy('config.json', 'dist/config.json')
        print(f"✅ config.json скопирован в dist/")
    else:
        print(f"⚠️  config.json не найден (будет создан при первом запуске)")

    print("\n📝 ИНСТРУКЦИЯ:")
    print("  1. Перейди в папку dist/")
    print("  2. Запусти Event_Reminder_System.exe")
    print("  3. config.json будет создан автоматически")
    print("  4. При необходимости отредактируй config.json")
else:
    print("❌ EXE файл не найден!")

print("="*60)
