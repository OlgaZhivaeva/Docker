FROM python:3.11-slim
WORKDIR /stocks_products/
COPY Django_project/3.2-crud/stocks_products /stocks_products
RUN pip install -r requirements.txt
RUN python manage.py migrate
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]