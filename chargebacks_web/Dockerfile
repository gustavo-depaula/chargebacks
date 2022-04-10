FROM python:3.10

# install poetry
RUN pip install poetry
WORKDIR /home/chargebacks
ADD pyproject.toml .
ADD poetry.lock .

RUN poetry install
CMD poetry run python manage.py runserver
# build with
# docker build -t chargebacks_web .
