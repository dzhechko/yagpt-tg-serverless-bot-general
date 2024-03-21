### Краткая информация
Telegram-бот на serverless-стеке Yandex Cloud, который использует YandexGPT при ответе на вопросы прользователей. 
Реализован с помощью библиотеки [python-telegram-bot](https://docs.python-telegram-bot.org/en/stable/index.html) на Python.
Данная версия бота не помнит предыдущие сообщения, поэтому решение задачи проводится в рамках текущего вопроса.

Настройки telegram-бота можно менять по своему усмотрению.

В стоимость ресурсов для приложения входят:
- Плата за "общение" с моделью YandexGPT (см. [тарифы YandexGPT](https://cloud.yandex.ru/ru/docs/yandexgpt/pricing))
- Плата за количество вызовов функции, вычислительные ресурсы, выделенные для выполнения функции, и исходящий трафик (см. [тарифы Yandex Cloud Functions](https://cloud.yandex.ru/ru/docs/functions/pricing)).
- Плата за количество запросов к API-шлюзу и исходящий трафик (см. [тарифы Yandex API Gateway](https://cloud.yandex.ru/ru/docs/api-gateway/pricing)).
- Плата за количество запросов к стандартной очереди (см. [тарифы Yandex Message Queue](https://cloud.yandex.ru/ru/docs/message-queue/pricing)).
- Плата за хранение и запрос секретов (см. [тарифы Yandex Lockbox](https://cloud.yandex.ru/ru/docs/lockbox/pricing)).

### Инструкция по развертыванию
1. Зарегистрируйте вашего бота в Telegram и получите токен:

1.1. Запустите бота BotFather и отправьте ему команду `/newbot`
1.2. Укажите имя вашего бота, например Serverless Echo Telegram Bot. Это имя будут видеть пользователи при общении с ботом.
1.3. Укажите имя пользователя вашего бота, например ServerlessHelloTelegramBot. По имени пользователя можно будет найти бота в Telegram. Имя пользователя должно оканчиваться на ...Bot или ..._bot.
На экране появится токен Telegram-бота.

2. [Создайте](https://cloud.yandex.ru/docs/lockbox/operations/secret-create) секрет Yandex Lockbox. Нужен секрет для телеграмм-бота и для YandexGPT. В поле Ключ секрета для телеграмм-бота укажите `TG_TOKEN`, в поле Значение — полученный токен Telegram-бота. Добавьте еще 2 пары Key-Value для YandexGPT, необходимо завести два Ключа и указать их значения: `YAGPT_FOLDER_ID` и `YAGPT_API_KEY`. Для получения `YAGPT_API_KEY` необходимо создать [сервисный аккаунт](https://cloud.yandex.ru/ru/docs/iam/quickstart-sa), которому должны быть назначены роли ai.languageModels.user для доступа к модели YandexGPT.

3. В [консоли](https://console.cloud.yandex.com/) управления выберите каталог, в котором хотите развернуть приложение.

4. Выберите сервис Cloud Apps.

5. На панели слева выберите Магазин приложений.

6. Выберите `Demo Telegram Bot YandexGPT` (или `Demo Telegram Bot`, но тогда придется добавить в проект все исходные файлы из данного репозитория и поменять среду исполнения на Python) и нажмите кнопку Использовать.

7. Укажите:

- Имя приложения.
- (Опционально) Описание приложения.
- Сервисный аккаунт с ролью admin на каталог или выберите Автоматически, чтобы нужный сервисный аккаунт создался при установке приложения. От имени этого сервисного аккаунта будут создаваться ресурсы приложения.
- Идентификатор секрета Yandex Lockbox, который создали ранее.

8. Нажмите кнопку Установить и дождитесь, пока приложение установится.

9. На странице Обзор, в разделе Ресурсы приложения, найдите API-шлюз, перейдите на его страницу и скопируйте ссылку на служебный домен.

10. Чтобы настроить связь между функцией и Telegram-ботом, выполните запрос. Вместо <токен бота> укажите токен Telegram-бота, вместо <домен API-шлюза> — ссылку на служебный домен API-шлюза.
- Для Linux/macOS
```
curl \
  --request POST \
  --url https://api.telegram.org/bot<токен бота>/setWebhook?url=https://<Домен API-шлюза>/echo
```
- Для Windows (cmd)
```
curl ^
  --request POST ^
  --url "https://api.telegram.org/bot<токен бота>/setWebhook?url=https://<Домен API-шлюза>/echo"
```
- Для Windows (Powershell)
```
curl.exe `
  --request POST `
  --url https://api.telegram.org/bot<токен бота>/setWebhook?url=https://<Домен API-шлюза>/echo
```

Результат:

{"ok":true,"result":true,"description":"Webhook was set"}

11. Напишите боту в Telegram.

### Полезные ссылки
- [Документация Yandex Cloud Functions](https://cloud.yandex.ru/ru/docs/functions/)
- [Документация Yandex API Gateway](https://cloud.yandex.ru/ru/docs/api-gateway/)
- [Документация Yandex Message Queue](https://cloud.yandex.ru/ru/docs/message-queue/)
- [Документация Yandex Lockbox](https://cloud.yandex.ru/ru/docs/lockbox/)
- [Документация YandexGPT API](https://cloud.yandex.ru/ru/docs/yandexgpt/)

Техническая поддержка
Служба технической поддержки Yandex Cloud отвечает на запросы 24 часа в сутки, 7 дней в неделю. Доступные виды запросов и срок их обработки зависят от тарифного плана. Подключить платную поддержку можно в [консоли управления](https://support.yandex.cloud/plans?section=plan). Подробнее о порядке оказания [технической поддержки](https://cloud.yandex.ru/ru/docs/support/overview).

### Ресурсы приложения
| Тип ресурса | Количество |
| ----------- | ----------- |
| Сервисные аккаунты	  | 4   |
| Статический ключ доступа  | 1   |
| Пользователи каталога | 7   |
| Message Queue	  | 1   |
| Бессерверная функция  | 1   |
| Триггер	   | 1   |
| API-шлюз  | 1   |
| YandexGPT API  | 1   |


### Лицензионное соглашение
Используя данный продукт, вы соглашаетесь с [Условиями использования Yandex Cloud Marketplace](https://yandex.ru/legal/cloud_terms_marketplace/)