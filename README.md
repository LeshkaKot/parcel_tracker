# Parcel Tracker API

Бекенд для відстеження поштових відправлень, побудований на Django + DRF.

## Стек
- Python 3.13
- Django 5.1
- Django REST Framework
- PostgreSQL
- Docker Compose

## Запуск проекту

### Через Docker 

1. Клонуй репозиторій:
```bash
git clone https://github.com/LeshkaKot/parcel_tracker.git
cd parcel_tracker
```

2. Створи `.env` файл на основі `.env.example`:
```bash
cp .env.example .env
```
(Заповни свої значення в `.env`.)

3. Запусти проект:
```bash
docker compose up --build
```

4. Створи суперкористувача :
```bash
docker compose exec web python manage.py createsuperuser
```

Проект доступний на `http://localhost:8000/api/`

### Локальний запуск

1. Створи та активуй віртуальне середовище:
```bash
python -m venv venv
venv\Scripts\activate  
```

2. Встанови залежності:
```bash
pip install -r requirements.txt
```

3. Створи `.env` файл та заповни дані БД.

4. Застосуй міграції:
```bash
python manage.py migrate
```

5. Запусти сервер:
```bash
python manage.py runserver
```

## Аутентифікація

Отримай токен:
POST /api/auth/token/
{"username": "...", "password": "..."}

Передавай токен у заголовку кожного запиту:

Authorization: Token <твій_токен>
GET запити доступні без токена (перегляд статусу посилки).

## Ендпоінти

| Метод | URL | Опис |
|-------|-----|------|
| POST | `/api/parcels/` | Створити посилку |
| GET | `/api/parcels/{tracking_number}/` | Деталі посилки + історія |
| POST | `/api/parcels/{tracking_number}/status/` | Змінити статус |
| GET | `/api/offices/{id}/parcels/` | Посилки у відділенні |
| GET | `/api/parcels/?status=&from_city=` | Список з фільтрацією |

## Бізнес-правила

- Трек-номер генерується автоматично у форматі `UA` + 10 символів
- `delivered` можливий лише після `arrived` у відділенні призначення
- `delivered` та `returned` - кінцеві статуси, зміна неможлива
- Вага: від 0 до 30 кг
- Відділення відправлення та призначення не можуть збігатися

## Статуси посилки

| Статус | Опис |
|--------|------|
| `created` | Зареєстровано |
| `accepted` | Прийнято у відділенні |
| `in_transit` | У дорозі |
| `arrived` | Прибула у відділення призначення |
| `delivered` | Видано отримувачу |
| `returned` | Повернуто відправнику |

## Адмін панель

Доступна за адресою `/admin/` після створення суперкористувача.

## Postman колекція

Імпорт `postman_collection.json` у Postman для готових прикладів запитів.