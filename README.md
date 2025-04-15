## Aplikacja webowa do dzielenia się artykułami i komunikacji w czasie rzeczywistym. Projekt demonstracyjny

# Technologie:
Backend

Flask – lekki framework w Pythonie

SQLAlchemy – ORM do obsługi bazy danych

SQLite – baza danych

JWT + bcrypt – bezpieczna autoryzacja i haszowanie haseł

Frontend
HTML / CSS / JS – interfejs użytkownika (czysty JS, bez frameworków)

MQTT.js – obsługa MQTT po stronie klienta

Komunikacja w czasie rzeczywistym
MQTT – czat w czasie rzeczywistym (HiveMQ)

Flask-SocketIO – komentarze live

SSE (Server-Sent Events) – powiadomienia i subskrypcje

Zastosowanie protokołów komunikacyjnych:

HTTP – API do operacji CRUD

WebSockets – dwukierunkowa komunikacja na żywo

MQTT – czaty oparte na publish/subscribe

SSE – jednostronne powiadomienia serwera

 
Główne funkcje

Rejestracja, logowanie, zarządzanie kontem

Tworzenie i edycja artykułów (z podziałem na kategorie)

Komentarze i system lajków na żywo

Czat z MQTT

Subskrypcje i powiadomienia

Wyszukiwanie i filtrowanie treści
