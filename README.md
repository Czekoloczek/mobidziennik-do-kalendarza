# mobidziennik-do-kalendarza

## Eksportuje twój plan lekcji z platformy mobiDziennik i zapisuje go w pliku w formacie .ics.

Możesz użyć owego pliku w **[Kalendarzu Google](https://support.google.com/calendar/answer/37118?hl=pl)**, **[Microsoft Outlook](https://support.microsoft.com/pl-pl/office/importuj-kalendarze-do-programu-outlook-8e8364e1-400e-4c0f-a573-fe76b5a2d379)** i innych kalendarzach, aby zaimportować swoje lekcje.

### Szybki dostęp:
- [Jak korzystać?](#jak-korzystać) - Dowiedz się jak poprawnie użyć programu.
- [Jak skompilować?](#jak-skompilować) - Dowiedz się jak samemu skompilować program. (Informacje przydatne głównie dla deweloperów i osób, które chcą wprowadzić zmiany w kodzie)

### Jak korzystać?

1. Pobierz plik mobidziennik.exe z [najnowszego wydania](https://github.com/JakubKoralewski/mobidziennik-do-kalendarza/releases/latest).

2. Uruchom plik, a następnie podaj subdomenę twojej szkoły na mobiDzienniku.
   - Aby zdobyć subdomenę, sprawdź, jak wygląda URL, po wejściu na dziennik. Dla mnie URL to `https://lo1olesnica.mobidziennik.pl`, więc wpiszę `lo1olesnica`.

3. Wpisz login, bądź adres e-mail (jeśli dodałeś go do swojego konta na mobiDzienniku) i hasło.
   - Program potrzebuje tych danych, aby wyświetlić stronę twojego planu lekcji na mobiDzienniku, aby następnie owe lekcje wyeksportować.

4. Jeśli wszystko wpisałeś poprawnie w tym samym folderze, w którym uruchomiłeś plik pokaże się plik calendar.ics. Są to twoje wyeksportowane lekcje, które możesz dodać do innego kalendarza.

> [!TIP]
> Subdomena i login/e-mail są zapisywane w pliku config.yaml, przy ponownym uruchomieniu programu, możesz nacisnąć enter, aby użyć zapisanych danych. Hasło nie jest zapisywane ze względów bezpieczeństwa.


> [!WARNING]
> **Program nie śledzi zastępstw, odwołań lekcji itp. Program **może** przestać działać po jakiejkolwiek zmianie w mobiDzienniku wykonanej przez WizjaNet.**

### Jak skompilować?

1. Zainstaluj Python ze strony https://www.python.org/downloads/.
> [!NOTE]
> Program był testowany na wersji 3.8, 3.10, 3.12. Zalecamy pobranie najnowszej wersji.

2. Otwórz CMD w folderze, w którym jest skrypt mobidziennik.py. Możesz to zrobić, wchodząc w owy folder w eksploratorze plików i wpisując `cmd` w pasku ścieżki folderu lub użyć komendy `cd` w CMD.

2. Aby skompilować kod, potrzebujesz następujących dependencji:
  - robobrowser
  - werkzeug 0.16.1
  - pyyaml
  - icalendar
  - pyinstaller
Możesz użyć tej komendy `pip install robobrowser werkzeug==0.16.1 pyyaml icalendar pyinstaller`, aby je wszystkie zainstalować.

> [!WARNING]
> Najnowsza wersja `werkzeug` nie jest kompatybilna z `robobrowser`, zalecamy pobranie wersji 0.16.1 dla `werkzeug`.

4. Użyj komendy `pyinstaller --onefile mobidziennik.py`, a następnie poczekaj, aż kompilator skończy pracę.
