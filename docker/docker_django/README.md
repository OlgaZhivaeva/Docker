Типовые команды для запуска контейнера c backend-сервером

docker build -t my-docker-django:first .

docker run -d --rm -p 8000:8000 my-docker-django:first

