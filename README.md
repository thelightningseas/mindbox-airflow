# mindbox-airflow

# Конфигурация

- Хранение метадаты - Postgrees
- Executor задач - Celery
- Мониторинг и жизненный цикл - Flower
- Брокер задач - redis

# Что еще изменил по сравнению с дефолтным композом из туториала:
- Добавил вольюм ```- /var/run/docker.sock:/var/run/docker.sock``` чтобы запускать докер задачки
- Добавил вольюм ```- /tmp:/tmp``` - его биндит эйрфлоу чтобы запустить там контейнер
- Зафиксировал версии имаджей
- Зафиксировал реквайрменты для воркеров
- Возможность скейлить воркеров

# Подготовка

1. На мастер ноду перенести ```docker-compose.yml```
2. Создать вольюмы для ассетов и результатов: 
- ```docker volume create results```
- ```docker volume create assets```
3. Заинитить airflow: ```docker-compose up -d --scale workers=3```
4. Если хотим ставить воркеров на других тачках, запускать только сервис ```workers``` с нужным скейлом и прописать пути до мастер ноды в конфиге
5. Если нужны ассеты, положить их в ```var/lib/docker/volumes/assets/_data``` на всех воркерах
6. Результаты пересчетов кладутся в ```var/lib/docker/volumes/results/_data```

# Использование

- На мастер ноде и воркерах есть папка ```dags```, в ней должен быть код пайплайнов
- На тачках с воркерами должен быть собран имадж ```optimal_sending_time```
- UI эйрфлоу: http://10.136.0.71:8080/home (креды airflow/airflow)
- Посмотреть воркеров: http://10.136.0.71:5555/

Код пайплайнов в репе лежит в dags
