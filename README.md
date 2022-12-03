Во первыых строках заявляю, проект сделан для того чтобы ускорить процесс настройки автотестов на вашем локальном проекте. То есть взяли скачали настроили запустили
1. Что нужно сделать перетйи на сайт и скачать Python 3.9 https://www.python.org/downloads/release/python-390/ и установить
2. Установить Pycharm https://www.jetbrains.com/pycharm/download/#section=windows
3. Клонировать этот проект себе
4. Открыть проект в Pycharm
5. Установить зависимости командой в терминале pip3 install -r requirements.txt   ![image](https://user-images.githubusercontent.com/82027564/205441398-64433aa4-512f-4552-af41-29db7d309154.png) если не установилось то нужно перейти в Interpreter Settings и установить вручную ![image](https://user-images.githubusercontent.com/82027564/205441457-50c97d83-da9f-4499-a7b0-741479f2c89f.png)

6. Для тестирования в файле теста нужно указать url и url_path ![image](https://user-images.githubusercontent.com/82027564/205441577-b788302d-51d3-4ed2-8047-5cd0e62aa176.png)


**helpers** — различные вспомогательные функции.

**locators** — тут хранятся все локаторы. 
**globals.py** — общие локаторы для всего сайта.

**pages** — тут хранитра структура всех страниц, на которых запускаются тесты.
**base_page.py** — page-object которые используются по всему сайту.
