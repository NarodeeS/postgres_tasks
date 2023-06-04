## Описание
Данный проект представляет собой систему для решения задач по PostgreSQL. Преподаватель может добавлять задания (описание, структура базы данных), а другие пользователи решать их с помощью интерактивной SQL-консоли.
<br>
## Использование
### На локальной машине
1. Создать файл ".env" в корне проекта и указать в нем актуальные значения переменных из ".env.sample".
2. Также указать в файле ".env.production" в директории "postgres_front" параметры для Vue.js.
3. Запустить скрипт: "build_and_start_all.sh".

### В Kubernetes кластере
Запустить скрипт "install.sh" в директории "kubernetes"

В любом случае будет необходимо создать суперпользователя Django. Теперь можно авторизоваться в admin-панели по адресу "адрес_сервера/admin" и создавать задания.
<br>
[Документация API](https://documenter.getpostman.com/view/23412097/2s93RNyaXz)
