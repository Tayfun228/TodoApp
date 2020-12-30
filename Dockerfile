FROM python:3.7

COPY requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip install -r requirements.txt
ADD . .

# CMD ["gunicorn", "--bind", "0.0.0.0", "-p", "8000", "todo.wsgi"]
# CMD ["export", "DJANGO_SETTINGS_MODULE=todo.settings"]
# CMD ["daphne", "todo.asgi:application"]
# CMD ["daphne", "-b", "0.0.0.0", "-p", "8000","todo.asgi:application"]





# RUN apt -y update
# RUN apt install -y python3
# RUN apt install -y python3-pip
# # RUN pip 3 



# WORKDIR /code
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0
# RUN apk add --no-cache gcc musl-dev linux-headers
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt
# EXPOSE 5000
# COPY . .
# CMD ["python3", "manage.py","runserver"]
