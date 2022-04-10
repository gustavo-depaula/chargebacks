FROM python:3.10

# install poetry
RUN pip install poetry
WORKDIR /home/chargebacks
ADD pyproject.toml .
ADD poetry.lock .

RUN poetry install
ENV PYTHONUNBUFFERED 1

CMD poetry run python manage.py runserver 0.0.0.0:8000

# build with
# docker build -t chargebacks_web .
