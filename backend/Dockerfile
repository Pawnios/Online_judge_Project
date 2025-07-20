

# RUN apt-get update && apt-get install -y clang
# WORKDIR /app
# COPY . /app
# RUN pip install --no-cache -r requirements.txt
# RUN python3 manage.py makemigrations
# RUN python3 manage.py migrate
# EXPOSE 8000

# ENV DJANGO_SETTINGS_MODULE=backend.settings
# ENV PYTHONUNBUFFERED=1

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM python:3.9

RUN apt-get update && apt-get install -y clang postgresql-client
WORKDIR /app
COPY . /app
RUN pip install --no-cache -r requirements.txt

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=backend.settings
ENV PYTHONUNBUFFERED=1

# Use entrypoint script instead of direct command
CMD ["./entrypoint.sh"]
