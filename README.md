# cbr_rates_python

Запуск на тестовом локальном сервере:
1. Склонировать репозиторий в рабочую директорию:
```bash
git clone https://github.com/flintpnz/cbr_rates_python.git
```
2. Создать virtualenv:
```bash
python -m venv venv
```
3. Активировать virtualenv:
```bash
(win) venv\Scripts\Activate.ps1
(nix) source venv/bin/activate
```
4. Установить зависимости:
```bash
pip install -r requirements.txt
```
5. Запустить тестовый сервер:
```bash
python manage.py runserver
```
6. Enjoy http://127.0.0.1:8000