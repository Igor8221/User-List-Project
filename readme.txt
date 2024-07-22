# Разработка первого приложения на FastAPI

## Инструкция по запуску приложения

1. **Создание виртуального окружения**

   Для разных операционных систем команды различаются:

   - Windows: `python -m venv venv`
   - Mac/Linux: `python -m venv venv` или `python3 -m venv venv`

2. **Активация виртуального окружения:**

   - Windows: `./venv/Scripts/activate`
   - Linux/Mac: `source venv/bin/activate`

3. **Установка зависимостей**

   Установите зависимости из файла `requirements.txt` в виртуальное окружение:

   ```bash
   pip install -r requirements.txt
   ```

4. **Переход в директорию приложения**

   Перейдите в директорию `app` с помощью команды:

   ```bash
   cd app
   ```

5. **Запуск приложения**

   Запустите главный файл приложения:

   ```bash
   python main.py
 
   python -m src.main
   ```


6. **Поздравляем!** Сервер успешно запущен.