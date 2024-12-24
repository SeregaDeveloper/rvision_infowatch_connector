# Интеграционный скрипт R-Vision InfoWatch

Этот скрипт интегрирует InfoWatch с R-Vision для автоматизации процесса получения событий из InfoWatch, их обработки и отправки в R-Vision.

## Требования

- Python 3.x
- Необходимые пакеты Python: `requests`, `configparser`, `zipfile`, `json`, `os`, `time`, `datetime`

## Установка

1. Клонируйте репозиторий или скачайте файлы скрипта.
    ```sh
    git clone 
    ```
2. Установите необходимые пакеты Python с помощью pip:
    ```sh
    pip install requests
    ```

## Конфигурация

1. Скопируйте файл [`settings.ini.template`](settings.ini.template ) в `settings.ini`:
    ```sh
    cp settings.ini.template settings.ini
    ```
2. Отредактируйте файл `settings.ini`, чтобы включить ваши учетные данные и настройки InfoWatch и R-Vision:
    ```ini
    [infowatch]
    url = ваш_url_infowatch
    username = ваш_логин_infowatch
    password = ваш_пароль_infowatch
    query_id = ваш_id_запроса

    [rvision]
    url = ваш_url_rvision
    key = ваш_api_ключ_rvision
    ```

## Использование

Запустите скрипт с помощью Python:
```sh
python rvision_infowatch.py

Sure, here is the 

README.md

 translated into Russian:

```md
# Интеграционный скрипт R-Vision InfoWatch

Этот скрипт интегрирует InfoWatch с R-Vision для автоматизации процесса получения событий из InfoWatch, их обработки и отправки в R-Vision.

## Требования

- Python 3.x
- Необходимые пакеты Python: `requests`, `configparser`, `zipfile`, `json`, `os`, `time`, `datetime`

## Установка

1. Клонируйте репозиторий или скачайте файлы скрипта.
2. Установите необходимые пакеты Python с помощью pip:
    ```sh
    pip install requests
    ```

## Конфигурация

1. Скопируйте файл [`settings.ini.template`](settings.ini.template ) в `settings.ini`:
    ```sh
    cp settings.ini.template settings.ini
    ```
2. Отредактируйте файл `settings.ini`, чтобы включить ваши учетные данные и настройки InfoWatch и R-Vision:
    ```ini
    [infowatch]
    url = ваш_url_infowatch
    username = ваш_логин_infowatch
    password = ваш_пароль_infowatch
    query_id = ваш_id_запроса

    [rvision]
    url = ваш_url_rvision
    key = ваш_api_ключ_rvision
    ```

## Использование

Запустите скрипт с помощью Python:
```sh
python rvision_infowatch.py
```

Скрипт выполнит следующие действия:

1. Аутентифицируется в InfoWatch.
2. Выполнит преднастроенный запрос для получения событий.
3. Обработает полученные события и классифицирует их.
4. Отправит обработанные события в R-Vision.
5. Сгенерирует и загрузит отчеты по событиям.

## Логирование

Скрипт записывает ошибки и важную информацию в файл `log.txt`. Проверьте этот файл на наличие проблем или важных сообщений.

## Структура файлов

- [`rvision_infowatch.py`](rvision_infowatch.py ): Основной файл скрипта.
- [`settings.ini.template`](settings.ini.template ): Шаблон файла конфигурации.
- `settings.ini`: Файл конфигурации (создается из шаблона).
- `log.txt`: Файл для логирования ошибок и информации.

## Лицензия

Этот проект лицензирован по лицензии MIT. См. файл LICENSE для получения подробной информации.

## Вклад

Приветствуются любые вклады! Пожалуйста, откройте issue или отправьте pull request для любых улучшений или исправлений ошибок.

## Контакты

Для любых вопросов или поддержки, пожалуйста, свяжитесь по адресу [your_email@example.com](mailto:your_email@example.com).
```