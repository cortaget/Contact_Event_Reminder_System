═══════════════════════════════════════════════════════════════════════
EVENT REMINDER SYSTEM - QUICK START GUIDE
═══════════════════════════════════════════════════════════════════════
Verze: 1.0 | Datum: 12.01.2026 | Autor: Maxim Mazuret

═══════════════════════════════════════════════════════════════════════
RYCHLÝ START - JAK SPUSTIT APLIKACI
═══════════════════════════════════════════════════════════════════════

KROK 1: KONTROLA POŽADAVKŮ
---------------------------
Před spuštěním ověřte, že máte nainstalováno:

✅ SQL Server 2016+ nebo SQL Server Express (ZDARMA)
   Stáhnout: https://www.microsoft.com/sql-server/sql-server-downloads
   
✅ ODBC Driver 17 for SQL Server
   Stáhnout: https://go.microsoft.com/fwlink/?linkid=2249004


KROK 2: SPUŠTĚNÍ APLIKACE
--------------------------

1. Dvakrát klikněte na Event_Reminder_System.exe(/dist)

2. Při PRVNÍM spuštění se zobrazí okno "Konfigurace databáze":

   ┌─────────────────────────────────────────────────┐
   │ ⚙️ Konfigurace databáze                         │
   ├─────────────────────────────────────────────────┤
   │ SQL Server: [ .\SQLEXPRESS                 ]    │
   │ Název databáze: [ Contact_Event_Reminder_S... ] │
   │ ODBC Driver: [ ODBC Driver 17 for SQL Server ]  │
   │ ☑ Použít Windows Authentication                 │
   │                                                  │
   │ [🔍 Otestovat připojení]                        │
   │ [✅ Uložit a pokračovat]                        │
   └─────────────────────────────────────────────────┘

3. Do pole "SQL Server" zadejte:
   - Pokud máte SQL Server Express: .\SQLEXPRESS
   - nebo jine co je potreba

4. Klikněte "Otestovat připojení"
   → Musí se zobrazit: ✅ Připojení úspěšné!(po prvnim spusteni databaze jeste neexistuje, zmacknete Uložit a pokračovat)

5. Klikněte "Uložit a pokračovat"

6. HOTOVO! Databáze se vytvoří automaticky a aplikace se spustí


═══════════════════════════════════════════════════════════════════════
ALTERNATIVNÍ METODA: SPUŠTĚNÍ Z PYTHONU (PRO VÝVOJÁŘE)
═══════════════════════════════════════════════════════════════════════

Pokud máte zdrojové kódy a chcete spustit aplikaci přes Python:

KROK 1: INSTALACE PYTHONU
--------------------------
1. Stáhněte Python 3.10 nebo novější:
   https://www.python.org/downloads/

2. Při instalaci ZAŠKRTNĚTE: "Add Python to PATH"

3. Ověřte instalaci (otevřete CMD):
   python --version
   → Mělo by zobrazit: Python 3.10.x nebo vyšší


KROK 2: INSTALACE ZÁVISLOSTÍ
-----------------------------
1. Otevřete příkazový řádek (CMD) nebo PowerShell

2. Přejděte do složky s projektem:
   cd C:\cesta\k\projektu\Event_Reminder_System

3. Nainstalujte požadované knihovny:
   pip install -r requirements.txt

   Instaluje se:
   • customtkinter==5.2.2  (GUI framework)
   • pyodbc==5.0.1         (SQL Server připojení)
   • Pillow==10.2.0        (zpracování obrázků)
   • python-dateutil==2.8.2 (práce s datumy)

4. Počkejte cca 1-2 minuty na dokončení instalace
═══════════════════════════════════════════════════════════════════════
POKROČILÁ KONFIGURACE (soubor config.json)
═══════════════════════════════════════════════════════════════════════


STRUKTURA SOUBORU:
{
    "database": {
        "server": ".\\SQLEXPRESS",
        "database": "Contact_Event_Reminder_System",
        "driver": "ODBC Driver 17 for SQL Server",
        "trusted_connection": true
    },
    "settings": {
        "default_reminder_days": 7
    }
}

POPIS PARAMETRŮ:
----------------

1. SERVER - Název SQL Server instance
Kde najít:
Varianta A: SQL Server Management Studio (SSMS)
Otevřete SSMS


V okně připojení vidíte název serveru nahoře


Formát: .\SQLEXPRESS nebo LOCALHOST\SQLEXPRESS nebo NázevPočítače\SQLEXPRESS


Varianta B: PowerShell/Příkazový řádek
powershell
sqlcmd -L

Zobrazí seznam všech SQL Server instancí v síti.
Varianta C: Services (Služby)
Stiskněte Win + R → napište services.msc


Hledejte službu SQL Server (SQLEXPRESS) nebo SQL Server (MSSQLSERVER)


Název v závorkách je název instance


Formáty:
. nebo localhost nebo (local) - lokální server


.\SQLEXPRESS - lokální pojmenovaná instance


192.168.1.10 nebo server.domena.cz - vzdálený server



2. DATABASE - Název databáze
Kde najít:
V SQL Server Management Studio:
Připojte se k serveru


Rozbalte složku Databases


Vidíte seznam všech databází


Poznamenejte si přesný název (case-sensitive!)


PowerShell:
powershell
sqlcmd -S .\SQLEXPRESS -Q "SELECT name FROM sys.databases"


3. DRIVER - ODBC ovladač
​
Kde zjistit nainstalované ovladače:
Varianta A: ODBC Data Source Administrator
powershell
odbcad32

Otevře se okno "Správce zdrojů dat ODBC"


Karta Drivers (Ovladače)


Hledejte: ODBC Driver 17 for SQL Server nebo ODBC Driver 18 for SQL Server


Varianta B: PowerShell
powershell
Get-OdbcDriver | Where-Object {$_.Name -like "*SQL Server*"}

Pokud ovladač NENÍ nainstalovaný:
Stáhněte a nainstalujte:
​
ODBC Driver 17: https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server


Spusťte instalátor .exe


Po instalaci ověřte příkazem odbcad32


Podporované názvy:
ODBC Driver 17 for SQL Server ✅


ODBC Driver 18 for SQL Server ✅


SQL Server (starší nativní ovladač)



4. TRUSTED_CONNECTION - Typ autentizace
Co to znamená:
true = Windows Authentication (integrovaná autentizace, bez hesla)


false = SQL Server Authentication (vyžaduje username + password)


Jak zjistit jaký typ použít:
Windows Authentication (true):
Používá vaše přihlášení k Windows


NEPOTŘEBUJE username/password


Funguje pouze pokud SQL Server povoluje Windows autentizaci


Bezpečnější pro lokální aplikace


SQL Server Authentication (false):
Používá SQL Server účty (např. sa)


VYŽADUJE username a password


Musí být povoleno v SQL Serveru


Kontrola v SSMS:
Pravý klik na server → Properties


Stránka Security


Podívejte se na Server authentication:


Windows Authentication mode - pouze Windows účty


SQL Server and Windows Authentication mode - obojí ✅



5. USERNAME - Uživatelské jméno
Defaultní účty:
sa - System Administrator (výchozí admin účet)


Vaše vlastní SQL Server účty (ve skole je to heslo je student)


Kde najít seznam účtů (v SSMS):
Rozbalte Security → Logins


Vidíte seznam všech uživatelů


Poznamenejte si přesné jméno


6. PASSWORD - Heslo
Pro účet sa:
Heslo jste nastavili při instalaci SQL Serveru




7. DEFAULT_REMINDER_DAYS - Nastavení aplikace
Toto je parametr vaší aplikace, NENÍ součástí SQL Serveru:
7 = zobrazit připomínky 7 dní dopředu


Můžete nastavit libovolné číslo



PŘÍKLADY KONFIGURACE:
---------------------
LOKÁLNÍ SQL EXPRESS (nejčastější):
{
    "database": {
        "server": ".\\SQLEXPRESS",
        ...
    }
}


═══════════════════════════════════════════════════════════════════════
⚠️ ŘEŠENÍ PROBLÉMŮ (pokud aplikace nefunguje)
═══════════════════════════════════════════════════════════════════════

PROBLÉM 1: Aplikace se nespustí - chybí soubory
------------------------------------------------
Chyba: "VCRUNTIME140.dll was not found"

ŘEŠENÍ:
→ Stáhněte Microsoft Visual C++ Redistributable:
  https://aka.ms/vs/17/release/vc_redist.x64.exe
→ Nainstalujte a restartujte počítač


PROBLÉM 2: Chyba "Nelze se připojit k serveru"
-----------------------------------------------
Chyba: "08001 Cannot connect to SQL Server"

ŘEŠENÍ:
A) Zkontrolujte, že SQL Server běží:
   1. Win + R → services.msc → Enter
   2. Najděte "SQL Server (SQLEXPRESS)" nebo "SQL Server (MSSQLSERVER)"
   3. Pokud je "Stopped" → Pravý klik → Start

B) Ověřte název serveru:
   1. Otevřete SQL Server Management Studio (SSMS)
   2. V dialogu připojení vidíte název serveru
   3. Zkopírujte ho do config.json (pole "server")

C) Zkontrolujte TCP/IP protokol:
   1. Otevřete "SQL Server Configuration Manager"
   2. SQL Server Network Configuration → Protocols for SQLEXPRESS
   3. TCP/IP → Enable


PROBLÉM 3: Chyba "Login failed" (18456)
----------------------------------------
Chyba: "18456 Login failed for user"

ŘEŠENÍ:
A) Použijte Windows Authentication:
   V config.json: "trusted_connection": true

B) Udělte oprávnění:
   1. Otevřete SSMS jako administrátor
   2. Security → Logins → Najděte svůj Windows účet
   3. Pravý klik → Properties → User Mapping
   4. Zaškrtněte databázi Contact_Event_Reminder_System
   5. Role: db_owner


PROBLÉM 4: Chyba "Cannot open database" (4060)
-----------------------------------------------
Chyba: "4060 Cannot open database Contact_Event_Reminder_System"

ŘEŠENÍ:
A) Databáze neexistuje - vytvořte ji:
   1. V aplikaci: Levé menu → "Nastavení"
   2. Klikněte "🔄 Inicializovat databázi"
   3. Potvrďte

B) Nebo ručně v SSMS:
   1. Otevřete soubor config.sql v SSMS
   2. Stiskněte F5 (Execute)


PROBLÉM 5: ODBC Driver není nainstalován
-----------------------------------------
Chyba: "Data source name not found"

ŘEŠENÍ:
→ Stáhněte a nainstalujte ODBC Driver 17:
  https://go.microsoft.com/fwlink/?linkid=2249004
→ Po instalaci restartujte aplikaci


PROBLÉM 6: Připomínky se nezobrazují
-------------------------------------
Připomínky fungují, ale žádné se neobjeví

ŘEŠENÍ:
A) Zkontrolujte datum události:
   - Musí být v BUDOUCNOSTI
   - Musí být <= "Dní předem" od dnešního data
   
B) Zkontrolujte notification tabulku:
   V SSMS:
   SELECT * FROM notification WHERE event_id = [ID_UDÁLOSTI]
   → Pokud existuje záznam status='sent' pro dnes, připomínka se již zobrazila


PROBLÉM 7: Import CSV nefunguje
--------------------------------
Chyba při importu CSV souboru

ŘEŠENÍ:
CSV soubor MUSÍ mít tyto sloupce (přesně takto):
first_name,last_name,birth_date,gender

Příklad správného CSV:
first_name,last_name,birth_date,gender
Jan,Novák,1990-05-15,male
Marie,Svobodová,1985-12-20,female

Poznámky:
- První řádek = názvy sloupců (POVINNÉ)
- Datum formát: YYYY-MM-DD
- Gender: male / female / other (nebo prázdné)


═══════════════════════════════════════════════════════════════════════
KONTAKT A PODPORA
═══════════════════════════════════════════════════════════════════════

Autor: Maxim Mazuret
Email: cortaget@gmail.com
Škola: Střední průmyslová škola elektrotechnická, Praha 2, Ječná 30
Verze: 1.0
Datum: 11.01.2026

Jedná se o školní projekt vytvořený pro předmět PV.

═══════════════════════════════════════════════════════════════════════
