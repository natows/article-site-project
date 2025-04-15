**Aplikacja webowa do dzielenia się artykułami i komunikacji w czasie rzeczywistym.**  
Projekt demonstracyjny zrealizowany w celach nauki backendu prezentujący zastosowanie różnych protokołów komunikacyjnych w nowoczesnej aplikacji webowej.

---

## Technologie

### Backend
- **Flask** – lekki framework w Pythonie
- **SQLAlchemy** – ORM do obsługi bazy danych
- **SQLite** – prosta, lokalna baza danych
- **JWT + bcrypt** – autoryzacja i bezpieczne haszowanie haseł

### Frontend
- **HTML / CSS / JavaScript** – interfejs użytkownika, bez użycia frameworków
- **MQTT.js** – obsługa protokołu MQTT po stronie klienta

### Komunikacja w czasie rzeczywistym
- **MQTT** – czat w czasie rzeczywistym (broker: HiveMQ)
- **Flask-SocketIO** – komentarze i interakcje live
- **SSE (Server-Sent Events)** – powiadomienia i aktualizacje subskrypcji

---

## Zastosowane protokoły

- **HTTP** – klasyczne REST API dla operacji CRUD
- **WebSockets** – dwukierunkowa komunikacja na żywo (np. komentarze)
- **MQTT** – publish/subscribe (np. czat)
- **SSE** – jednostronna komunikacja serwera z klientem (np. powiadomienia)

---

## Główne funkcje

- Rejestracja, logowanie, zarządzanie kontem użytkownika  
- Tworzenie, edycja i usuwanie artykułów z podziałem na kategorie  
- Komentarze w czasie rzeczywistym wraz z systemem polubień  
- Czat tematyczny oparty o MQTT  
- Subskrypcje i system powiadomień  
- Wyszukiwanie i filtrowanie artykułów  
