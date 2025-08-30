Files_Bot
Files_Bot — асинхронный Python-бот для автоматизированной публикации файлов из Google Drive в Telegram-канал с расширенными фильтрами, кастомизацией и поддержкой CI/CD через Docker и GitHub Actions.

💡 Возможности
Мониторинг Google Drive — автоматически сканирует папки, забирает новые файлы по расписанию.

Гибкие фильтры — поддержка фильтрации по размеру, mime-type и маскам имени файла.

Перенос файлов — скачивает, публикует в указанный Telegram-канал, удаляет исходник при успехе.

Гибкая настройка источников — работает с несколькими аккаунтами/дисками.

Асинхронность — максимум производительности без блокирования.

Полная контейнеризация — простейший запуск через Docker Compose.

CI/CD — автоматический деплой через GitHub Actions по пушу в main.

Хранение и учёт — все метаданные файлов и статус операций — в PostgreSQL.

🚀 Быстрый старт
1. Клонирование репозитория
bash
git clone https://github.com/Ale007XD/Files_Bot.git
cd Files_Bot
2. Заполнение конфигурации
Создайте файлы cred.json для каждого Google Drive-источника в gdrive_credentials/.

Скопируйте и отредактируйте пример:

bash
cp sources.yaml.example sources.yaml
nano sources.yaml
Пример содержимого:

text
sources:
  - source_id: "gdrive_john"
    credentials_path: "/app/gdrive_credentials/john.json"
    drive_folders:
      - "FOLDER_ID1"
    author_tag: "#john"
    filters:
      min_size: 100000
      include_mime: ["image/", "video/"]
3. Настройка переменных окружения (обязательно для prod!)
См. список переменных в docker-compose.yml и .github/workflows/deploy.yml (BOT_TOKEN, TELEGRAM_CHANNEL_ID и т.д.).

4. Сборка и запуск (Docker Compose)
bash
docker-compose up --build -d
Система автоматически поднимет PostgreSQL и бот-контейнер. Все миграции — автосоздание бекенда.

⚙️ Структура проекта
text
.
├── app/
│   ├── config.py          # конфигурация, парсинг yaml
│   ├── db.py              # асинхронный SQLAlchemy
│   ├── drive.py           # работа с Google Drive
│   ├── jobs.py            # бизнес-логика, воркеры
│   ├── main.py            # точка входа, asyncio-loop
│   ├── models.py          # модель File
│   ├── telegram.py        # отправка в Telegram
│   └── utils.py           # утилиты, фильтры, caption
├── sources.yaml.example   # пример конфига источников
├── requirements.txt       # зависимости pip
├── Dockerfile             # сборка контейнера
├── docker-compose.yml     # сборка и оркестрация
├── .github/workflows/
│   └── deploy.yml         # CI/CD деплой на сервер
└── (README.md)            # этот файл
🗂 Описание параметров
sources.yaml (каждый блок в sources):

source_id — уникальный id источника (логическая метка).

credentials_path — путь до сервисного ключа Google (JSON).

drive_folders — список Google Drive folder IDs.

author_tag — тег автора (для подписи и фильтрации).

filters — опциональные ограничения:

min_size — минимальный размер файла (в байтах)

include_mime — фильтрация по mime-type

exclude_mask — маски на название файла (не обязательны)

Подробнее — смотрите и дополняйте sources.yaml.example.

📝 Использование вне Docker (для разработки)
Создайте .env или экспортируйте переменные окружения.

Установите зависимости:

bash
pip install -r requirements.txt
Запуск:

bash
python -m app.main
🏗 CI/CD, деплой и обновление
Автоматический деплой — срабатывает на push в main, использует github secrets для секретных ключей, деплоит на сервер через SSH + rsync + docker-compose.

Переменные продакшна и секреты — задаются только на стороне CI/CD.

🐞 Отладка и Логирование
Поддержка уровней логирования через переменную окружения LOG_LEVEL (по-умолчанию INFO).

Все критические ошибки — логируются и помечаются в базе.

📢 Обратная связь и доработка
Issues — открыты для багов/фич/вопросов.

Предложения и PR приветствуются!

📃 Лицензия
MIT (можно использовать, изменять, распространять без ограничений).
