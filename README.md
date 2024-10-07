# mobidziennik-do-kalendarza

## Eksportuje twój plan lekcji z platformy mobiDziennik i zapisuje go w pliku w formacie .ics.

Możesz użyć owego pliku w **Kalendarzu Google**, **Microsoft Outlook** i innych kalendarzach, aby zaimportować swoje lekcje.

### Jak korzystać?

1. Pobierz plik mobidziennik.exe z [najnowszego wydania](https://github.com/JakubKoralewski/mobidziennik-do-kalendarza/releases/latest).

2. Uruchom plik, a następnie podaj subdomenę twojej szkoły na mobiDzienniku.
   - Aby zdobyć subdomenę sprawdź jak wygląda URL, po wejściu na dziennik. Dla mnie URL to `https://lo1olesnica.mobidziennik.pl`, więc wpiszę `lo1olesnica`.

3. Wpisz login, bądź adres e-mail (jeśli dodałeś go do swojego konta na mobiDzienniku) i hasło.
   - Program potrzebuje tych danych, aby wyświetlić stronę twojego planu lekcji na mobiDzienniku, aby następnie owe lekcje wyeksportować.

4. Jeśli wszystko wpisałeś poprawnie w tym samym folderze, w którym uruchomiłeś plik pokaże się plik calendar.ics. Są to twoje wyeksportowane lekcje, które możesz dodać do innego kalendarza.

> [!TIP]
> Subdomena i login/e-mail są zapisywane w pliku config.yaml, przy ponownym uruchomieniu programu, możesz nacisnąć enter, aby użyć zapisanych danych. Hasło nie jest zapisywane ze względów bezpieczeństwa.


> [!WARNING]
> **Pogram nie śledzi zastępstw, odwołań lekcji, itp. Program **może** przestać działać po jakiejkolwiek zmianie w mobiDzienniku wykonanej przez WizjaNet.**
