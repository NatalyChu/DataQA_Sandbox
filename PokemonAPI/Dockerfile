FROM apache/airflow:2.8.1

# Копируем requirements под root
USER root
COPY requirements.txt /requirements.txt
RUN chmod 644 /requirements.txt
USER airflow

# Устанавливаем пакеты от имени airflow (правильный способ)
RUN pip install --no-cache-dir -r /requirements.txt

# Копируем DAGs
COPY dags /opt/airflow/dags