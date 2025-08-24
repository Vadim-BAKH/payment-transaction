# Backend. Асинхронное веб-приложение в парадигме REST API

Приложение эммулирует некоторые настройки платёжной системы.


## Стэк и зависимости.

Для разработки приложения используется Python версии 12 и выше. В контейнере - python:3.12.3-bookworm

Приложение разрабатывается с FastApi, SQLAlchemy ORM, PostgreSQL.

Все зависимости указаны в pyproject.toml.


## Окружение.

Клонирование приложения:

          git clone git@github.com:Vadim-BAKH/payment-transaction.git

Перейти в папку payment-transaction и создать виртуальное окружение (если еще не создано):

          poetry init

Активировать виртуальное окружение для доступа к зависимостям приложения:

          source .venv/bin/activate

Убедиться, что в .gitignore внесены .env и certs/.

В корне проекта создать папку .env c переменными окружения по образцу файла .env.template.

В корне проекта создать папку certs/. Выполнить команды:

           mkdir certs && cd certs
           openssl genrsa -out jwt-private.pem 2048
           openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem

Убедитесь, что ключи - серые - не подсвечены, как и .env.


## Запуск приложения

Приложение запускается в контейнере. Для перевой сборки выполнить команду:

           docker compose up --build -d   (Интерактивно для просмотра логов запуск без -d)

Альтернативно возможен запуск приложения из файла **alternative_run_appl.py**.

           Для этого необходимо изменить конфигурацию хоста в .env c
           APP_CONFIG__DB__URL=postgresql+asyncpg://superuser:mypassword@db:5432/main_db
           на
           APP_CONFIG__DB__URL=postgresql+asyncpg://superuser:mypassword@localhost:5432/main_db
           Выполнить запуск postgres:
           docker compose up db -d
           Выполнить:
           python fastapi_app/alternative_run_appl.py

При запуске приложения автоматически создаются адимнистратор-superuser, пользователь-test_user и его account-балансовый счёт с остатоком 0.

Для работы с данными сущностями используйте данные из .env, например:

          # Настройки администратора
          APP_CONFIG__SUPERUSER__EMAIL=admin@example.com
          APP_CONFIG__SUPERUSER__PASSWORD=supersecret123
          APP_CONFIG__SUPERUSER__FIRST_NAME=Admin
          APP_CONFIG__SUPERUSER__LAST_NAME=Root

          # Настройки тестового пользователя
          APP_CONFIG__TEST_USER__EMAIL=test@example.com
          APP_CONFIG__TEST_USER__PASSWORD=test1234
          APP_CONFIG__TEST_USER__FIRST_NAME=Test
          APP_CONFIG__TEST_USER__LAST_NAME=Test


## Техническое задание.

Необходимо реализовать работу со следующими сущностями:
Пользователь
Администратор
Счет - имеет баланс, привязан к пользователю
Платеж(пополнение баланса) - хранит уникальный идентификатор и сумму пополнения счета пользователя

Пользователь должен иметь следующие возможности:
Авторизоваться по email/password
Получить данные о себе(id, email, full_name)
Получить список своих счетов и балансов
Получить список своих платежей

Администратор должен иметь следующие возможности:
Авторизоваться по email/password
Получить данные о себе (id, email, full_name)
Создать/Удалить/Обновить пользователя
Получить список пользователей и список его счетов с балансами

Для работы с платежами должен быть реализован роут эмулирующий обработку вебхука от сторонней платежной системы.
Структура json-объекта для обработки вебхука должна состоять из следующих полей:
transaction_id - уникальный идентификатор транзакции в “сторонней системе”
account_id - уникальный идентификатор счета пользователя
user_id - уникальный идентификатор счета пользователя
amount - сумма пополнения счета пользователя
signature - подпись объекта

signature должна формироваться через SHA256 хеш, для строки состоящей из конкатенации значений объекта в алфавитном порядке ключей и “секретного ключа” хранящегося в конфигурации проекта ({account_id}{amount}{transaction_id}{user_id}{secret_key}).

Пример, для secret_key gfdmhghif38yrf9ew0jkf32:
{
  "transaction_id": "5eae174f-7cd0-472c-bd36-35660f00132b",
  "user_id": 1,
  "account_id": 1,
  "amount": 100,
  "signature": "7b47e41efe564a062029da3367bde8844bea0fb049f894687cee5d57f2858bc8"
}

При обработке вебхука необходимо:
Проверить подпись объекта
Проверить существует ли у пользователя такой счет - если нет, его необходимо создать
Сохранить транзакцию в базе данных
Начислить сумму транзакции на счет пользователя

Транзакции являются уникальными, начисление суммы с одним transaction_id должно производиться только один раз.

Для тестирования приложения в миграции должен быть создан:
Тестовый пользователь
Счет тестового пользователя
Тестовый администратор


## Примеры реализации.

Любой авторизованный пользователь может пройти аутентификацию и авторизоваться.

В данный момент входит администратор. У него роль superuser, ресурс super, право на действие main:

<img width="1920" height="933" alt="image" src="https://github.com/user-attachments/assets/22ee0f50-7392-480c-87ad-b61f3a395b56" />

Администратор может зарегистрировать (создать) пользователя:

<img width="1909" height="1006" alt="image" src="https://github.com/user-attachments/assets/77e74500-a17b-45b6-ab65-4c909ae274bd" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/0fb0c33b-64dd-4537-a008-38050ba12329" />

Администратор может обновить пользователя по любому полю:

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/78431cbd-0253-4507-aff1-27006d1b97f8" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/8931609c-0784-4340-9a73-624472beebc6" />

Администратор может удалить пользователя (используется мягкое удаление - деактивация).

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/16e114ab-3ead-48c2-9ea5-928dd7d6449f" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/49acea04-d337-44dd-85c3-d5f944b791e1" />

В техзадании нет условия, но предусмотрено назначение администратором ролей, прав на действие для различных рессурсов, для любого пользователя.

Можно посмотреть какими правами и ресурсами располагает администратор:

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/292392a5-aae4-44ad-96fd-a5e4a13ff58d" />

Администратор, как и любой текущий активный пользователь может посмотреть информацию о себе.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/afc0b14c-b6f7-489b-97d0-eace03c55366" />

Может посмотреть свои счета, но у него их пока нет.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/9c5db815-d9a7-4f70-8c31-5305783b501a" />

Может посмотреть свои транзакции, но их пока нет.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/046bc238-5f02-4f22-9c46-be9c85bf22ff" />

Администратор может создать счёт любому пользователю и в том числе себе.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/08224a5d-9bc2-42a6-b31c-8ec5ebe8139a" />

По умолчанию, на счёте 0.

Если принять webhook-платеж по его счету:

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/e4e8a4ec-0908-405f-90b1-8246b38596d3" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/0149baed-c0d8-4239-8c24-f2ac39413e8d" />

Можно увидеть зачисление.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/dda46b7b-6311-4020-bab1-31e728dc00dc" />

Так же администратору доступен просмотр информации обо всех пользователях (активных и нет) с балансовыми счетами.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/da51fff1-f286-4918-9ad0-882974a45fae" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/38719724-af9a-4e32-bf55-331f444f3641" />

Рассмотрим что доступно любому активному текущему пользователю. Входим как test_user.

<img width="1920" height="568" alt="image" src="https://github.com/user-attachments/assets/5a0290c2-77f1-4dbe-93fa-80a8c6f85413" />

Просмотр информации о себе.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d6cf7a13-e8ff-4d4b-9377-130396ab3195" />

Просмотр своих **активных** счетов.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3f89e142-52a1-4ff0-bb58-dc59abdbe993" />

В данный момент есть счёт 8, который создал администратор, но на нем баланс 0.

Пополним этот счет.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/fc3934ec-ab5d-404c-83f1-75619db2d3c9" />

И пополним не существующий счет, что бы создался новый. Видим создался по порядку счет 11.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c2bfcd4a-e334-484b-a4ef-9953a9ec01d2" />

Можем снова проверить счета.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/dbeb1812-cb90-4a2f-93a9-ce05de9cd20b" />

Так же пользователь может посмотреть свои транзакции.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c52787c3-0cbe-4ec4-9c64-dbb66f7a5d2b" />

Но обычный пользователь не может получить доступ к тому, что позволено администратору.

Например, попытка доступа ко всем пользователям со счетами приведет к ошибке.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/15636ba3-61b8-4da2-b643-3f16a64e0431" />


## Тестирование

Проект включает конфигурацию для тестирования и автоматизации проверки кода.

- **Интеграционные тесты**:
  - Проверяют функциональность авторизации пользователя через JWT.
  - Тестируют получение данных текущего пользователя (`/api/auth/users/me`).
  - Проверяют работу с балансом пользователя и платежными транзакциями (`/api/accounts/look`, `/api/payments/look`).
  - Используют асинхронный HTTP-клиент (`httpx.AsyncClient`) и тестовую базу данных через фикстуры.
  - В тестах автоматически создаются пользователи и платежи для проверки бизнес-логики.

- **Фикстуры**:
  - `user_account` — создаёт тестового пользователя в базе.
  - `auth_token` — возвращает JWT access token для тестов.
  - `payment_fixture` — создаёт тестовые платежи и счета пользователя.

- **CI/CD**:
  - GitHub Actions workflow запускается на ветках `development` и `main`.
  - Проверяет код через `ruff`.
  - Строит и запускает Docker-контейнеры приложения.
  - Выполняет автоматические тесты через `pytest`.
  - После завершения workflow контейнеры останавливаются и удаляются.

> Тесты изолированы от продакшн-базы данных и используют тестовую среду для безопасного выполнения.


## Примечание.

Приложение реализовано в рамках технического задания, но предусматривает дальнейшее масштабирование проекта.
